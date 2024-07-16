let lineChart;

function setupLineChart() {
    let lineCtx = $('#lineChart')[0].getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'ms_10_10',
                borderWidth: 2,
                borderColor: 'blue',
                fill: false
            },
            {
                label: 'ms_10_30',
                borderWidth: 2,
                borderColor: 'green',
                fill: false
            },
            {
                label: 'ms_20_10',
                borderWidth: 2,
                borderColor: 'purple',
                fill: false
            },
            {
                label: 'ms_20_30',
                borderWidth: 2,
                borderColor: 'orange',
                fill: false
            },
            {
                label: 'ms_30_10',
                borderWidth: 2,
                borderColor: 'cyan',
                fill: false
            },
            {
                label: 'ms_30_30',
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
                    type: 'realtime',
                    realtime: {
                        duration: 30000,
                        refresh: 1000,
                        delay: 2000,
                        pause: false,
                        frameRate: 60,
                        onRefresh: function (matrixChart) {
                            fetchData();
                        }
                    },
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
            },
        }
    });
}

function updateLineChart(newData) {
    const now = new Date().getTime();
    lineChart.data.datasets[0].data.push({ x: now, y: newData.ms_10_10 });
    lineChart.data.datasets[1].data.push({ x: now, y: newData.ms_10_30 });
    lineChart.data.datasets[2].data.push({ x: now, y: newData.ms_20_10 });
    lineChart.data.datasets[3].data.push({ x: now, y: newData.ms_20_30 });
    lineChart.data.datasets[4].data.push({ x: now, y: newData.ms_30_10 });
    lineChart.data.datasets[5].data.push({ x: now, y: newData.ms_30_30 });
    lineChart.update('quiet');
}

window.setupLineChart = setupLineChart;
window.updateLineChart = updateLineChart;