let lineChart;

function convertTimestampToDate(timestamp) {
    date = new Date(timestamp * 1000);
    return date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
}

function setupHistoryLineChart(historyData) {
    let lineCtx = $('#historyLineChart')[0].getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: historyData.map(entry => convertTimestampToDate(entry.timestamp)),
            datasets: [{
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.data.filter(data => data.y == '5' && data.x == '10')[0].v
                })),
                label: 'ms_10_10',
                borderWidth: 2,
                borderColor: 'blue',
                fill: false
            },
            {
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.data.filter(data => data.y == '15' && data.x == '30')[0].v
                })),
                label: 'ms_10_30',
                borderWidth: 2,
                borderColor: 'green',
                fill: false
            },
            {
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.data.filter(data => data.y == '25' && data.x == '10')[0].v
                })),
                label: 'ms_20_10',
                borderWidth: 2,
                borderColor: 'purple',
                fill: false
            },
            {
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.data.filter(data => data.y == '25' && data.x == '30')[0].v
                })),
                label: 'ms_20_30',
                borderWidth: 2,
                borderColor: 'orange',
                fill: false
            },
            {
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.data.filter(data => data.y == '25' && data.x == '10')[0].v
                })),
                label: 'ms_30_10',
                borderWidth: 2,
                borderColor: 'cyan',
                fill: false
            },
            {
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.data.filter(data => data.y == '25' && data.x == '30')[0].v
                })),
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
                    title: {
                        display: true,
                        text: 'Time'
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
            animation: false
        }
    });
}

function fitChart() {
    var chartCanvas = document.getElementById('historyLineChart');
    var maxWidth = chartCanvas.parentElement.parentElement.clientWidth;
    var width = Math.max(lineChart.data.labels.length * 1.5, maxWidth);

    chartCanvas.parentElement.style.width = width + 'px';
}


async function updateHistoryLineChart(historyData) {
    if (lineChart == null || lineChart.data.datasets.length == 0) setupHistoryLineChart(historyData);

    lineChart.data.datasets[0].data = historyData.map(entry => entry.data.filter(data => data.y == '5' && data.x == '10')[0].v);
    lineChart.data.datasets[1].data = historyData.map(entry => entry.data.filter(data => data.y == '15' && data.x == '10')[0].v);
    lineChart.data.datasets[2].data = historyData.map(entry => entry.data.filter(data => data.y == '25' && data.x == '10')[0].v);
    lineChart.data.datasets[3].data = historyData.map(entry => entry.data.filter(data => data.y == '5' && data.x == '30')[0].v);
    lineChart.data.datasets[4].data = historyData.map(entry => entry.data.filter(data => data.y == '15' && data.x == '30')[0].v);
    lineChart.data.datasets[5].data = historyData.map(entry => entry.data.filter(data => data.y == '25' && data.x == '30')[0].v);
    lineChart.data.labels = historyData.map(entry => convertTimestampToDate(entry.timestamp));
    fitChart()
    lineChart.update();
}

window.setupHistoryLineChart = setupHistoryLineChart;
window.updateHistoryLineChart = updateHistoryLineChart;