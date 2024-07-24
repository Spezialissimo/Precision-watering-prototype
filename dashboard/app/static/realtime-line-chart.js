let lastSensorMap = {};
let lastUpdateTimeStamp = 0;

function setupRealtimeLineChart() {
    let lineCtx = $('#lineChart')[0].getContext('2d');
    let lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'ms_10_10',
                borderWidth: 2,
                borderColor: 'blue',
                fill: false,
                pointStyle: 'line',
                pointRadius: 0,
                tension: 0.4,  // Add this line
                cubicInterpolationMode: 'monotone'
            },
            {
                label: 'ms_10_30',
                borderWidth: 2,
                borderColor: 'green',
                fill: false,
                pointStyle: 'line',
                pointRadius: 0,
                tension: 0.4,  // Add this line
                cubicInterpolationMode: 'monotone'
            },
            {
                label: 'ms_20_10',
                borderWidth: 2,
                borderColor: 'purple',
                fill: false,
                pointStyle: 'line',
                pointRadius: 0,
                tension: 0.4,  // Add this line
                cubicInterpolationMode: 'monotone'
            },
            {
                label: 'ms_20_30',
                borderWidth: 2,
                borderColor: 'orange',
                fill: false,
                pointStyle: 'line',
                pointRadius: 0,
                tension: 0.4,  // Add this line
                cubicInterpolationMode: 'monotone'
            },
            {
                label: 'ms_30_10',
                borderWidth: 2,
                borderColor: 'cyan',
                fill: false,
                pointStyle: 'line',
                pointRadius: 0,
                tension: 0.4,  // Add this line
                cubicInterpolationMode: 'monotone'
            },
            {
                label: 'ms_30_30',
                borderWidth: 2,
                borderColor: 'magenta',
                fill: false,
                pointStyle: 'line',
                pointRadius: 0,
                tension: 0.4,  // Add this line
                cubicInterpolationMode: 'monotone'
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
                        refresh: 500,
                        delay: 2000,
                        pause: false,
                        frameRate: 30,
                        onRefresh: function (chart) {
                            chart.data.datasets[0].data.push({ x: lastUpdateTimeStamp, y: lastSensorMap["10-5"] });
                            chart.data.datasets[1].data.push({ x: lastUpdateTimeStamp, y: lastSensorMap["30-5"] });
                            chart.data.datasets[2].data.push({ x: lastUpdateTimeStamp, y: lastSensorMap["10-15"] });
                            chart.data.datasets[3].data.push({ x: lastUpdateTimeStamp, y: lastSensorMap["30-15"] });
                            chart.data.datasets[4].data.push({ x: lastUpdateTimeStamp, y: lastSensorMap["10-25"] });
                            chart.data.datasets[5].data.push({ x: lastUpdateTimeStamp, y: lastSensorMap["30-25"] });
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
            animation: false,
        }
    });
}

function updateRealtimeLineChart(newData) {
    const sensorMap = {};
    lastUpdateTimeStamp = (parseFloat(newData["timestamp"]) * 1000);
    newData["data"].forEach(sensor => {
        const key = `${sensor.x}-${sensor.y}`;
        sensorMap[key] = sensor.v;
    });
    lastSensorMap = sensorMap;
}

window.setupRealtimeLineChart = setupRealtimeLineChart;
window.updateRealtimeLineChart = updateRealtimeLineChart;