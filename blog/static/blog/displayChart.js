$(document).ready(function() {

    // Glucose Average by Day chart
     var avgByDayOptions = {
        chart: {
            renderTo: 'chart_panel',
            type: 'line',
        },
        legend: {enabled: false},
        title: {text: 'Monitoring Temperature Testeur'},
        subtitle: {text: '__'},
        xAxis: {title: {text: null}, labels: {rotation: -45}},
        yAxis: {title: {text: null}},
        series: [{}],
    };

    var chartDataUrl = "{% url 'call_fillChart' %}";
    $.getJSON(chartDataUrl,
        function(data) {
            avgByDayOptions.xAxis.categories = data['chart_data']['dates'];
            avgByDayOptions.series[0].name = 'Température moyenne (°C)';
            avgByDayOptions.series[0].data = data['chart_data']['values'];
            var chart = new Highcharts.Chart(avgByDayOptions);
    });
} );