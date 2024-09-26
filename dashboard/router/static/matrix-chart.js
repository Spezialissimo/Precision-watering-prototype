let matrixChart;

function convertToMatrixData(data) {
    return data["data"].map(obj => ({
        x: String(obj.x),
        y: String(obj.y),
        v: putMoistureValueInRange(Math.round(obj.v))
    }));
}

function setupMatrixChart(data) {
    const individualXs = [...new Set(data.data.map(element => String(element['x'])))].sort((a, b) => Number(b) - Number(a));
    const individualYs = [...new Set(data.data.map(element => String(element['y'])))].sort((a, b) => Number(a) - Number(b));
    let matrixCtx = $('#matrixChart')[0].getContext('2d');
    matrixChart = new Chart(matrixCtx, {
        type: "matrix",
        data: {
            datasets: [
                {
                    data: convertToMatrixData(data),
                    backgroundColor: function (context) {
                        if (!context.dataset || !context.dataset.data.length || context.dataset.data[context.dataIndex].v == null) return "lightgrey";
                        const value = context.dataset.data[context.dataIndex].v;
                        return getBackgroundColor(value);
                    },
                    width(c) {
                        const a = c.chart.chartArea || {};
                        return (a.right - a.left) / individualXs.length;
                    },
                    height(c) {
                        const a = c.chart.chartArea || {};
                        return (a.bottom - a.top) / individualYs.length;
                    }
                }
            ]
        },
        options: {
            scales: {
                y: {
                    type: "category",
                    labels: individualYs,
                    reverse: false,
                    offset: true,
                    ticks: {
                        stepSize: 5
                        // autoSkip: false
                    },
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                },
                x: {
                    type: "category",
                    labels: individualXs,
                    offset: true,
                    position: "bottom",
                    ticks: {
                        stepSize: 5,
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
                            return ["x: " + v.x, "y: " + v.y, "value: " + v.v];
                        }
                    }
                },
            },
            animation: false
        }
    });
}

function updateMatrixChart(data) {
    if (matrixChart == null) {
        setupMatrixChart(data);
    } else {
        matrixChart.data.datasets[0].data = convertToMatrixData(data);
    }
    matrixChart.update();
}

window.updateMatrixChart = updateMatrixChart;
