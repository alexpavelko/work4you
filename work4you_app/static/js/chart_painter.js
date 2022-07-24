function show_pie_chart(data, id, title, format, pointFormat) {
    Highcharts.chart(id, {
        chart: {
            type: 'pie'
        },
        title: {
            text: title
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    format: format
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:12px">{point.name}</span><br>',
            pointFormat: `<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> ${pointFormat}<br/>`
        },
        series: [
            {
                colorByPoint: true,
                data: data,
            }
        ]
    });
}

function show_column_chart(data, id, title, yAxisText, format, pointFormat) {
    console.log(data)
    Highcharts.chart(id, {
        chart: {
            type: 'column'
        },
        title: {
            text: title
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: yAxisText
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    format: format + pointFormat
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:13px">{category.name}</span><br>',
            pointFormat: `<span style="color:{point.color}">{point.name}</span>: <b>${format}</b>${pointFormat}<br/>`
        },
        series: [
            {
                colorByPoint: true,
                data: data,
            }
        ],
    });
}