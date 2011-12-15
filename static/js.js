
var chart;

var chartColors = [ '#699CC7', '#282687', '#387059', '#A58252', '#A64E29', '#EEBB76' ];

function loadChart() {
     if (chart) chart.destroy();

    $.ajax({
        url: 'data.csv',
        global: false,
        type: "GET",
        success: function(data) {

            chart = new Dygraph(document.getElementById("chart1"), data, {
                labelsDiv: document.getElementById(("chartLabel1")),
                labelsSeparateLines: false,
                width: 500,
                height: 500,
                highlightCircleSize: 0,
                fractions: false,
                wilsonInterval: false,
                includeZero: false,
                axisLineColor: '#C0C0C0',
                showRoller: false,
                drawXGrid: false,
                drawYGrid: false,
                logscale: false,
                fillGraph: true,
                connectSeparatedPoints: true,
                padding: { left: 0, right: 0, top: 0, bottom: 0 },
                axisLabelFontSize: 11,
                avoidMinZero: true,
                labelsKMB: false,
                xAxisLabelFormatter: Dygraph.dateAxisFormatter,
                colors: chartColors,
                yAxisLabelWidth: 0,
            });
        }
    });


};

setInterval(function() { loadChart(); }, 1000);
