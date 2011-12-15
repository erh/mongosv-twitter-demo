import sys
import pymongo
import json

import jinja2
from flask import Flask, render_template


app = Flask(__name__)

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
        

    last = live.find({'user.screen_name': {'$exists': True}})
    live.sort([('created_at', pymongo.DESCENDING)])
    live.limit(10)

    return render_template("index.html",
        mentions=mentions,
        posters=posters,
        last=last)


if __name__ == "__main__":
    debug = 'production' not in sys.argv

    app.run(host='0.0.0.0', debug=debug)
