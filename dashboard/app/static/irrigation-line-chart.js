let irrigationLineChart;

function convertTimestampToDate(timestamp) {
    date = new Date(timestamp * 1000);
    return date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
}

function setupIrrigationLineChart(historyData) {
    let lineCtx = $('#irrigationLineChart')[0].getContext('2d');
    irrigationLineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: historyData.map(entry => convertTimestampToDate(entry.timestamp)),
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

async function updateIrrigationLineChart(newData) {
    irrigationLineChart.data.datasets[0].data.push( { x: convertTimestampToDate(newData.timestamp), y: newData.optimal_m } );
    irrigationLineChart.data.datasets[1].data.push( { x: convertTimestampToDate(newData.timestamp), y: newData.current_m } );
    irrigationLineChart.data.labels.push(convertTimestampToDate(newData.timestamp));
    irrigationLineChart.update();
}

window.setupIrrigationLineChart = setupIrrigationLineChart;
window.updateIrrigationLineChart = updateIrrigationLineChart;