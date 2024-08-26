let lastSensorData = {};
let skippedCounter = 0;
let lineChart

function createRealTimeDatasetConfig(x, y, color) {
    return {
        label: "Sensore (" + x + ", " + y + ")",
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

function drawNewPoint(sensor_data, datasetIndex) {
    if (lineChart.data.datasets[datasetIndex].data.length > 2) {
        const lastDrawnData = lineChart.data.datasets[datasetIndex].data[lineChart.data.datasets[datasetIndex].data.length - 1];
        if (lastDrawnData.y != sensor_data.data[datasetIndex].v || skippedCounter >= 1) {
            lineChart.data.datasets[datasetIndex].data.push({ x: convertTimestampToDateForRealtime(sensor_data.timestamp), y: sensor_data.data[datasetIndex].v });
        } else {
            skippedCounter++;
        }
    }else {
        lineChart.data.datasets[datasetIndex].data.push({ x: convertTimestampToDateForRealtime(sensor_data.timestamp), y: sensor_data.data[datasetIndex].v });
    }
}

function setupRealtimeLineChart() {
    let lineCtx = $('#lineChart')[0].getContext('2d');
    lineChart = new Chart(lineCtx, {
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
                        refresh: 1000,
                        delay: 2000,
                        pause: false,
                        frameRate: 30,
                        onRefresh: async function (chart) {
                            try {
                                const response = await fetch('/sensors/');
                                lastSensorData = await response.json();
                                $('#syncingModal').modal('hide');
                            } catch (error) {
                                $('#syncingModal').modal('show');
                            }
                            if (lastSensorData == {} || lastSensorData.timestamp == undefined) {
                                return;
                            }
                            drawNewPoint(lastSensorData, 0);
                            drawNewPoint(lastSensorData, 1);
                            drawNewPoint(lastSensorData, 2);
                            drawNewPoint(lastSensorData, 3);
                            drawNewPoint(lastSensorData, 4);
                            drawNewPoint(lastSensorData, 5);
                        }
                    },
                    title: {
                        display: true,
                        text: 'Tempo (secondi)'
                    }
                },
                y: {
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Livello di umidità'
                    }
                }
            },
            animation: false,
        }
    });
}

window.setupRealtimeLineChart = setupRealtimeLineChart;