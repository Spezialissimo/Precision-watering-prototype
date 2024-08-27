let currentMatrixChart;
let currentOptimal;

function upsertIrrigationControls(optimal) {
    currentOptimal = optimal;
    if (optimal.id == get_optimal_from_name("disabled").id) {
        $('#irrigationControlContainer').empty().append(
            `<div class="w-100 h-100 align-content-center">
                <p class="text-center fw-bold">Disponibile solo in modalità automatica</p>
            </div>
            `);
        return;
    } else if (optimal.id == get_optimal_from_name("Slider").id) {
        setupOptimalSlider()
    } else {
        setupOptimalMatrixChart(optimal.value);
    }
}

function setupOptimalSlider() {
    $('#irrigationControlContainer').empty().append(
        `<div class="w-100 h-100 align-content-center">
        <label for="irrigationSlider" class="form-label w-100">Media di irrigazione richiesta: <span
            id="sliderValue">50</span></label>
        <input type="range" class="form-range w-50" id="irrigationSlider">
        `);

    value = Math.round(getLastOptimalMoistureValue());
    $('#irrigationSlider').val(value);
    $('#sliderValue').text(value);

    $('#irrigationSlider').on('change', function () {
        updateSliderValue($(this).val());
    });

    $('#irrigationSlider').on('input', function () {
        var value = $(this).val();
        $('#sliderValue').text(value);
    });
}

function setupOptimalMatrixChart(data) {
    const individualXs = [...new Set(data.data.map(element => String(element['x'])))].sort((a, b) => Number(a) - Number(b));
    const individualYs = [...new Set(data.data.map(element => String(element['y'])))].sort((a, b) => Number(a) - Number(b));

    $('#irrigationControlContainer').empty().append('<canvas id="optimalMatrixChart" height="400" width="400" style="max-height: 410px; max-width: 400px; display: initial;"></canvas>');

    let matrixCtx = $('#optimalMatrixChart')[0].getContext('2d');
    currentMatrixChart = new Chart(matrixCtx, {
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
                            return ["x: " + v.x, "y: " + v.y, "valore: " + v.v];
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


function setControlsMatrixChartMoinstureRange() {
    if (currentMatrixChart != null) {
        currentMatrixChart.update();
    }
}

window.setControlsMatrixChartMoinstureRange = setControlsMatrixChartMoinstureRange;