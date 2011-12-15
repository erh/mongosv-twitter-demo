import sys
import pymongo
import json

import jinja2
import flask


env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
app = flask.Flask(__name__)

db = pymongo.Connection().test
live = db.live

live.ensure_index( "created_at" )

@app.route("/")
def topData():

# ----------------------------------------------------------------------------------------

    if db.live.count() == 0:
        mentions = []
        posters = []
    else:
        mentions = live.inline_map_reduce( '''
function(){ 
    if ( ! ( this.entities && this.entities.user_mentions ) )
        return;

    var x = this.entities.user_mentions;

    for ( var i=0; i<x.length; i++ ) {
        emit( x[i].screen_name , 1 );
    }
}''' 
                                  ,
                                           
'''
function(k,arr) {
    return Array.sum(arr)
}
''' )
        
        mentions.sort( lambda a,b: int(b["value"] - a["value"]) )
        mentions = mentions[0:10]

# ----------------------------------------------------------------------------------------
        posters = db.command( "aggregate" , "live" ,
                              pipeline = [ 
                { "$match" : { "user.screen_name" : { "$exists" : True } } } , 
                { "$group" : { "_id" : "$user.screen_name" , "total" : { "$sum" : 1 } } } , 
                { "$sort" : { "total" : -1 } } , 
                { "$limit" : 10 } ] )["result"]
        
# ----------------------------------------------------------------------------------------
        

    pageParams = { "mentions" : mentions , "posters" : posters }

    pageParams["last"] = live.find( { "user.screen_name" : { "$exists" : True } } , 
                                    sort=[("created_at",pymongo.DESCENDING)] ).limit(10)

    return env.get_template( "index.html" , pageParams ).render( pageParams )


if __name__ == "__main__":
    debug = True
    for x in sys.argv:
        if x == "production":
            debug=False

    if debug:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0')
