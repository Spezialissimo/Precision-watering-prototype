let lineChart;

function setupLineChart() {
    let lineCtx = $('#lineChart')[0].getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 60 }, (_, i) => "-".concat((60 - i))),
            datasets: [{
                label: 'ms_10_10',
                data: Array.from({ length: 60 }, (_, i) => 0),
                borderWidth: 2,
                borderColor: 'blue',
                fill: false
            },
            {
                label: 'ms_10_30',
                data: Array.from({ length: 60 }, (_, i) => 0),
                borderWidth: 2,
                borderColor: 'green',
                fill: false
            },
            {
                label: 'ms_20_10',
                data: Array.from({ length: 60 }, (_, i) => 0),
                borderWidth: 2,
                borderColor: 'purple',
                fill: false
            },
            {
                label: 'ms_20_30',
                data: Array.from({ length: 60 }, (_, i) => 0),
                borderWidth: 2,
                borderColor: 'orange',
                fill: false
            },
            {
                label: 'ms_30_10',
                data: Array.from({ length: 60 }, (_, i) => 0),
                borderWidth: 2,
                borderColor: 'cyan',
                fill: false
            },
            {
                label: 'ms_30_30',
                data: Array.from({ length: 60 }, (_, i) => 0),
                borderWidth: 2,
                borderColor: 'magenta',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time (seconds)'
                    }
                },
                y: {
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Humidity level'
                    }
                }
            },
            animation: {
                duration: 0
            }
        }
    });
}

function updateLineChart(dataHistory) {
    lineChart.data.datasets[0].data = [...dataHistory.ms_10_10];
    lineChart.data.datasets[1].data = [...dataHistory.ms_10_30];
    lineChart.data.datasets[2].data = [...dataHistory.ms_20_10];
    lineChart.data.datasets[3].data = [...dataHistory.ms_20_30];
    lineChart.data.datasets[4].data = [...dataHistory.ms_30_10];
    lineChart.data.datasets[5].data = [...dataHistory.ms_30_30];

    lineChart.update();
}
