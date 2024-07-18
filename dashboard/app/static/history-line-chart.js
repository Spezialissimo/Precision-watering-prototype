let lineChart;

function convertTimestampToDate(timestamp) {
    date = new Date(timestamp * 1000);
    return date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
}

function setupHistoryLineChart(historyData) {
    const pointsOfInterest = {
        '10-5': [],
        '30-5': [],
        '10-15': [],
        '30-15': [],
        '10-25': [],
        '30-25': []
    };

    historyData.forEach(entry => {
        const timestamp = entry.timestamp;
        entry.data.forEach(sensor => {
            const key = `${sensor.x}-${sensor.y}`;
            if (pointsOfInterest.hasOwnProperty(key)) {
                pointsOfInterest[key].push({ x: timestamp, y: sensor.v });
            }
        });
    });

    let lineCtx = $('#historyLineChart')[0].getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: historyData.map(entry => convertTimestampToDate(entry.timestamp)),
            datasets: [{
                data: pointsOfInterest['10-5'],
                label: 'ms_10_10',
                borderWidth: 2,
                borderColor: 'blue',
                fill: false
            },
            {
                data: pointsOfInterest['30-5'],
                label: 'ms_10_30',
                borderWidth: 2,
                borderColor: 'green',
                fill: false
            },
            {
                data: pointsOfInterest['10-15'],
                label: 'ms_20_10',
                borderWidth: 2,
                borderColor: 'purple',
                fill: false
            },
            {
                data: pointsOfInterest['10-25'],
                label: 'ms_20_30',
                borderWidth: 2,
                borderColor: 'orange',
                fill: false
            },
            {
                data: pointsOfInterest['30-15'],
                label: 'ms_30_10',
                borderWidth: 2,
                borderColor: 'cyan',
                fill: false
            },
            {
                data: pointsOfInterest['30-25'],
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
    var width = Math.max(lineChart.data.labels.length * 2, maxWidth);

    chartCanvas.parentElement.style.width = width + 'px';
}


async function updateHistoryLineChart(historyData) {
    if (lineChart == null) setupHistoryLineChart(historyData);
    const pointsOfInterest = {
        '10-5': [],
        '30-5': [],
        '10-15': [],
        '30-15': [],
        '10-25': [],
        '30-25': []
    };

    historyData.forEach(entry => {
        const timestamp = entry.timestamp;
        entry.data.forEach(sensor => {
            const key = `${sensor.x}-${sensor.y}`;
            if (pointsOfInterest.hasOwnProperty(key)) {
                pointsOfInterest[key].push({ x: convertTimestampToDate(timestamp), y: sensor.v });
            }
        });
    });

    lineChart.data.datasets[0].data = pointsOfInterest['10-5'];
    lineChart.data.datasets[1].data = pointsOfInterest['30-5'];
    lineChart.data.datasets[2].data = pointsOfInterest['10-15'];
    lineChart.data.datasets[3].data = pointsOfInterest['30-15'];
    lineChart.data.datasets[4].data = pointsOfInterest['10-25'];
    lineChart.data.datasets[5].data = pointsOfInterest['30-25'];
    lineChart.data.labels = historyData.map(entry => convertTimestampToDate(entry.timestamp));

    fitChart()
    lineChart.update();
}

window.setupHistoryLineChart = setupHistoryLineChart;
window.updateHistoryLineChart = updateHistoryLineChart;