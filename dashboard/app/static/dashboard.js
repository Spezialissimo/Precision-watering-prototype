$(document).ready(function () {
    setupRealtimeLineChart();
    setupMatrixChart();

    function fetchData() {
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

    function fetchInterpolatedData() {
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

    function fetchHistoryData() {
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

    window.fetchData = fetchData;
    $('#togglePump').click(function () {
        fetch('/togglePump');
    });
    $('#refreshHistory').click(function () {
        fetchHistoryData();
    });

    fetchData();
    fetchHistoryData();
    fetchInterpolatedData();
    setInterval(fetchData, 500);
    setInterval(fetchInterpolatedData, 100);
});
