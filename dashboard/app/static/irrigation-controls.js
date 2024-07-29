function upsertIrrigationControls(optimal) {
    if(optimal == Optimals.Disabled) {
        $('#irrigationControlContainer').empty().append(
            `<div class="w-100 h-100 align-content-center">
                <h2 class="text-center fw-bold">Disabled</h2>
            </div>
            `);
        return;
    } else if (optimal == Optimals.Slider) {
        setupOptimalSlider()
    } else {
        fetch(optimal.value_uri)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                setupOptimalMatrixChart(data);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }
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
        v: obj.v
    }));
}

function setupOptimalSlider() {
    $('#irrigationControlContainer').empty().append(
        `<div class="w-100 h-100 align-content-center">
        <label for="irrigationSlider" class="form-label w-100">Media di irrigazione richiesta: <span
            id="sliderValue">50</span></label>
        <input type="range" class="form-range w-50" id="irrigationSlider">
        `);
}

function setupOptimalMatrixChart(data) {
    const individualXs = [...new Set(data.data.map(element => String(element['x'])))].sort((a, b) => Number(a) - Number(b));
    const individualYs = [...new Set(data.data.map(element => String(element['y'])))].sort((a, b) => Number(a) - Number(b));

    $('#irrigationControlContainer').empty().append('<canvas id="optimalMatrixChart" height="400" width="400" style="max-height: 400px; max-width: 400px; display: initial;"></canvas>');

    let matrixCtx = $('#optimalMatrixChart')[0].getContext('2d');
    new Chart(matrixCtx, {
        plugins: [ChartDataLabels],
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
                        autoSkip: false
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
                        autoSkip: false,
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
                                return { weight: 'bold' };
                            },
                            formatter(value) {
                                return value.v;
                            }
                        }
                    }
                }
            },
            animation: false
        }
    });
}