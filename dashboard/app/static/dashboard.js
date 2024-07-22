$(document).ready(function () {
    setupRealtimeLineChart();

    async function fetchData() {
        fetch('/getLastReadings')
            .then(response => response.json())
            .then(data => {
                updateRealtimeLineChart(data);

                if ($('#syncingModal').is(':visible')) {
                    $('#syncingModal').modal('hide');
                }
            })
            .catch(error => {
                if (!$('#syncingModal').is(':visible')) {
                    $('#syncingModal').modal('show');
                }
            });
    }

    async function fetchInterpolatedData() {
        fetch('/getLastReadingsWithInterpolation')
            .then(response => response.json())
            .then(data => {
                updateMatrixChart(data);
            })
            .catch(error => {
                if (!$('#syncingModal').is(':visible')) {
                    $('#syncingModal').modal('show');
                }
            });
    }

    async function fetchHistoryData() {
        fetch('/getHistory?seconds=600')
            .then(response => response.json())
            .then(data => {
                updateHistoryLineChart(data);
            })
            .catch(error => {
                if (!$('#syncingModal').is(':visible')) {
                    $('#syncingModal').modal('show');
                }
            });
    }

    async function fetchIrrigationData() {
        fetch('/getIrrigationData')
            .then(response => response.json())
            .then(data => {
                updateIrrigationLineChart(data);
            })
            .catch(error => {
                if (!$('#syncingModal').is(':visible')) {
                    $('#syncingModal').modal('show');
                }
            });
    }

    async function fetchAllIrrigationData() {
        fetch('/getIrrigationHistoryData?seconds=600')
            .then(response => response.json())
            .then(data => {
                setupIrrigationLineChart(data);
            })
            .catch(error => {
                if (!$('#syncingModal').is(':visible')) {
                    $('#syncingModal').modal('show');
                }
            });
    }

    $('#togglePump').click(function () {
        fetch('/togglePump');
    });

    $('#refreshHistory').click(function () {
        fetchHistoryData();
    });

    $('#irrigationSlider').on('change', function () {
        var value = $(this).val();
        fetch('/setIrrigation?value=' + value, { method: 'POST' });
    });

    $('#irrigationSlider').on('input', function () {
        var value = $(this).val();
        $('#sliderValue').text(value);
    });

    fetchData();
    fetchHistoryData();
    fetchInterpolatedData();
    fetchAllIrrigationData();
    setInterval(fetchData, 1000);
    setInterval(fetchInterpolatedData, 500);
    setInterval(fetchIrrigationData, 5000);
});
