let irrigationLineChart;
let lastIrrigationData;
let didUsePreview = false;

function normalizeIrrigationValue(value, maxIrrigationValue) {
    return ((value) / maxIrrigationValue) * 100;
}

function setupIrrigationLineChart(historyData, maxIrrigationValue = 15) {
    let lineCtx = $('#irrigationLineChart')[0].getContext('2d');
    lastIrrigationData = historyData[historyData.length - 1];
    irrigationLineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            datasets: [
                {
                    data: historyData.map(entry => ({
                        x: convertTimestampToDateForRealtime(entry.timestamp),
                        y: entry.optimal_m
                    })),
                    label: 'Umidità ottimale',
                    borderWidth: 3,
                    borderColor: 'blue',
                    fill: false,
                    pointStyle: 'line',
                    pointRadius: 0,
                    tension: 0.4,
                    cubicInterpolationMode: 'monotone'
                },
                {
                    data: historyData.map(entry => ({
                        x: convertTimestampToDateForRealtime(entry.timestamp),
                        y: entry.current_m
                    })),
                    label: 'Umidità attuale',
                    borderWidth: 3,
                    borderColor: 'cyan',
                    fill: false,
                    pointStyle: 'line',
                    pointRadius: 0,
                    tension: 0.4,
                    cubicInterpolationMode: 'monotone'
                },
                {
                    type: 'bar',
                    label: 'Consiglio irriguo',
                    data: historyData.map(entry => ({
                        x: convertTimestampToDateForRealtime(entry.timestamp),
                        y: normalizeIrrigationValue(entry.irrigation, maxIrrigationValue),
                        rawValue: 0.03 * entry.irrigation
                    })),
                    backgroundColor: 'rgba(0, 0, 128, 0.2)',
                    datalabels: {
                        display: true,
                        align: 'start',
                        anchor: 'end',
                        clamp: true,
                        formatter: function (value) {
                            if (value.rawValue == null || value.rawValue == "") {
                                return '';
                            }
                            return value.rawValue.toFixed(2);
                        },
                        color: 'black',
                        offset: 0
                    }
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                datalabels: {
                    display: false
                }
            },
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        duration: 120000,
                        refresh: 1000,
                        delay: 0,
                        pause: false,
                        frameRate: 30,
                        onRefresh: async function (chart) {
                            try {
                                const response = await fetch('/irrigation/');
                                lastIrrigationData = await response.json();
                            } catch (error) {
                                $('#syncingModal').modal('show');
                            }

                            if(lastIrrigationData == null) {
                                return;
                            }

                            const newTimestamp = convertTimestampToDateForRealtime(lastIrrigationData.timestamp);
                            const dataset = irrigationLineChart.data.datasets;

                            shouldUpdate = didUsePreview ? newTimestamp == dataset[0].data[dataset[0].data.length - 2].x : newTimestamp == dataset[0].data[dataset[0].data.length - 1].x;
                            if (newTimestamp == dataset[0].data[dataset[0].data.length - 1].x) {
                                return;
                            }


                            if (dataset[2].data.length === 0 || dataset[2].data[dataset[2].data.length - 1].x < newTimestamp) {
                                dataset[2].data.push({
                                    x: newTimestamp,
                                    y: normalizeIrrigationValue(lastIrrigationData.irrigation, 15),
                                    rawValue: 0.03 * lastIrrigationData.irrigation
                                });

                                if (!didUsePreview) {
                                    dataset[0].data.push({ x: newTimestamp, y: putMoistureValueInRange(lastIrrigationData.optimal_m) });
                                }
                                didUsePreview = false;
                                dataset[1].data.push({ x: newTimestamp, y: putMoistureValueInRange(lastIrrigationData.current_m) });
                                irrigationLineChart.update();
                            }
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
                },
                y1: {
                    beginAtZero: true,
                    min: 0,
                    max: 0.45,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Consiglio irriguo (litri)'
                    },
                    grid: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                },
            },
            animation: false
        },
        plugins: [ChartDataLabels]
    });
}

function updateOptimalIrrigationLine(value) {
    if (didUsePreview) {
        irrigationLineChart.data.datasets[0].data.pop();
    }
    const lastDrawnData = irrigationLineChart.data.datasets[0].data[irrigationLineChart.data.datasets[0].data.length - 1];
    irrigationLineChart.data.datasets[0].data.push({ x: lastDrawnData.x + 15000, y: putMoistureValueInRange(value) });
    didUsePreview = true;
    irrigationLineChart.update();
}

function getLastOptimalMoistureValue() {
    return putMoistureValueInRange(lastIrrigationData.optimal_m);
}

function setIrrigationLineChartMoinstureRange() {
    irrigationLineChart.update();
}

window.setIrrigationLineChartMoinstureRange = setIrrigationLineChartMoinstureRange;
window.setupIrrigationLineChart = setupIrrigationLineChart;
window.getLastOptimalMoistureValue = getLastOptimalMoistureValue;
