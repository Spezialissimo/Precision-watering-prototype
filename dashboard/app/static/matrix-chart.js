let matrixChart;

function setupMatrixChart() {
    let matrixCtx = $('#matrixChart')[0].getContext('2d');
    matrixChart = new Chart(matrixCtx, {
        plugins: [ChartDataLabels],
        type: "matrix",
        data: {
            datasets: [
                {
                    data: [],
                    backgroundColor: function (context) {
                        if (!context.dataset || !context.dataset.data.length || context.dataset.data[context.dataIndex].v == null) return "lightgrey";
                        const value = context.dataset.data[context.dataIndex].v;
                        return getBackgroundColor(value);
                    },
                    width(c) {
                        const a = c.chart.chartArea || {};
                        return (a.right - a.left) / 5;
                    },
                    height(c) {
                        const a = c.chart.chartArea || {};
                        return (a.bottom - a.top) / 5;
                    }
                }
            ]
        },
        options: {
            scales: {
                y: {
                    type: "category",
                    reverse: false,
                    offset: true,
                    labels: ["5", "10", "15", "20", "25"],
                    ticks: {
                        autoSkip: true
                    },
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                },
                x: {
                    type: "category",
                    offset: true,
                    position: "bottom",
                    labels: ["10", "15", "20", "25", "30"],
                    ticks: {
                        autoSkip: true,
                        maxRotation: 0,
                    },
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                }
            },
            plugins: {
                legend: false,
                tooltip: {
                    callbacks: {
                        title() {
                            return "";
                        },
                        label(context) {
                            const v = context.dataset.data[context.dataIndex];
                            return ["x: " + v.x, "y: " + v.y, "v: " + v.v];
                        }
                    }
                },
                datalabels: {
                    labels: {
                        value: {
                            color() {
                                return 'black';
                            },
                            font() {
                                weight: 'bold'
                            },
                            formatter(value) {
                                return value.v;
                            }
                        }
                    }
                }
            },
            animation: {
                duration: 0
            }
        }
    });
}

function updateMatrixChart(data) {
    matrixChart.data.datasets[0].data = convertToMatrixData(data);
    matrixChart.update();
}

function getBackgroundColor(value) {
    const startColor = { r: 178, g: 34, b: 34 };
    const endColor = { r: 0, g: 0, b: 255 };
    const r = startColor.r + (endColor.r - startColor.r) * (value / 100);
    const g = startColor.g + (endColor.g - startColor.g) * (value / 100);
    const b = startColor.b + (endColor.b - startColor.b) * (value / 100);
    return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
}

function convertToMatrixData(data) {
    return data["data"].map(obj => ({
        x: String(obj.x),
        y: String(obj.y),
        v: String(obj.v)
    }));
}

window.setupMatrixChart = setupMatrixChart;
window.updateMatrixChart = updateMatrixChart;