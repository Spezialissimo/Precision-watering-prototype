let irrigationLineChart;

function convertTimestampToDate(timestamp) {
    return luxon.DateTime.fromSeconds(timestamp).toJSDate();
}

function setupIrrigationLineChart(historyData) {
    let lineCtx = $('#irrigationLineChart')[0].getContext('2d');
    irrigationLineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            datasets: [{
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.optimal_m
                })),
                label: 'Optimal',
                borderWidth: 2,
                borderColor: 'blue',
                fill: false
            },
            {
                data: historyData.map(entry => ({
                    x: convertTimestampToDate(entry.timestamp),
                    y: entry.current_m
                })),
                label: 'Current',
                borderWidth: 2,
                borderColor: 'cyan',
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second',
                        tooltipFormat: 'HH:mm:ss' // Format per le etichette
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

async function updateIrrigationLineChart(newData) {
    const newTimestamp = convertTimestampToDate(newData.timestamp);
    const dataset = irrigationLineChart.data.datasets;

    if (dataset[0].data.length === 0 || dataset[0].data[dataset[0].data.length - 1].x < newTimestamp) {
        dataset[0].data.push({ x: newTimestamp, y: newData.optimal_m });
        dataset[1].data.push({ x: newTimestamp, y: newData.current_m });
        irrigationLineChart.update();
    }
}

window.setupIrrigationLineChart = setupIrrigationLineChart;
window.updateIrrigationLineChart = updateIrrigationLineChart;
