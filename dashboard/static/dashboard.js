$(document).ready(function () {
    setupLineChart();
    setupMatrixChart();

    function fetchData() {
        fetch('/getLastReadings')
            .then(response => response.json())
            .then(data => {
                if (data.timestamp == null) throw new Error("Error fetching data");
                console.log("Fetched data: ", data);

                updateLineChart(data);
                updateMatrixChart(data);

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

    window.fetchData = fetchData;
    $('#togglePump').click(function () {
        fetch('/togglePump');
    });

    fetchData();
    setInterval(fetchData, 500);
});


