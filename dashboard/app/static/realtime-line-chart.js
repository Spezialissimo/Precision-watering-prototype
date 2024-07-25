let lastSensorData = {};

function createRealTimeDatasetConfig(x, y, color) {
    return {
        label: "Sensor (" + x + ", " + y + ")",
        data: [],
        borderWidth: 2,
        borderColor: color,
        fill: false,
        pointStyle: 'line',
        pointRadius: 0,
        tension: 0.4,
        cubicInterpolationMode: 'monotone'
    }
}

function setupRealtimeLineChart() {
    let lineCtx = $('#lineChart')[0].getContext('2d');
    let lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            datasets: [
                createRealTimeDatasetConfig('10', '5', 'blue'),
                createRealTimeDatasetConfig('10', '15', 'purple'),
                createRealTimeDatasetConfig('10', '25', 'cyan'),
                createRealTimeDatasetConfig('30', '5', 'green'),
                createRealTimeDatasetConfig('30', '15', 'orange'),
                createRealTimeDatasetConfig('30', '25', 'magenta'),
            ]
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
                        onRefresh: async function (chart) {
                            try {
                                const response = await fetch('/getLastReadings');
                                lastSensorData = await response.json();
                                $('#syncingModal').modal('hide');
                            } catch (error) {
                                $('#syncingModal').modal('show');
                            }
                            if (lastSensorData == {} || lastSensorData.timestamp == undefined) {
                                return;
                            }
                            chart.data.datasets[0].data.push({ x: convertTimestampToDateForRealtime(lastSensorData.timestamp), y: lastSensorData.data[0].v });
                            chart.data.datasets[1].data.push({ x: convertTimestampToDateForRealtime(lastSensorData.timestamp), y: lastSensorData.data[1].v });
                            chart.data.datasets[2].data.push({ x: convertTimestampToDateForRealtime(lastSensorData.timestamp), y: lastSensorData.data[2].v });
                            chart.data.datasets[3].data.push({ x: convertTimestampToDateForRealtime(lastSensorData.timestamp), y: lastSensorData.data[3].v });
                            chart.data.datasets[4].data.push({ x: convertTimestampToDateForRealtime(lastSensorData.timestamp), y: lastSensorData.data[4].v });
                            chart.data.datasets[5].data.push({ x: convertTimestampToDateForRealtime(lastSensorData.timestamp), y: lastSensorData.data[5].v });
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

window.setupRealtimeLineChart = setupRealtimeLineChart;