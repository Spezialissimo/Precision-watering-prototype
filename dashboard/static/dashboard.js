$(document).ready(function () {
    setupLineChart();
    setupMatrixChart();

    let dataHistory = {
        ms_10_10: Array.from({ length: 60 }, (_, i) => 0),
        ms_10_30: Array.from({ length: 60 }, (_, i) => 0),
        ms_20_10: Array.from({ length: 60 }, (_, i) => 0),
        ms_20_30: Array.from({ length: 60 }, (_, i) => 0),
        ms_30_10: Array.from({ length: 60 }, (_, i) => 0),
        ms_30_30: Array.from({ length: 60 }, (_, i) => 0),
    };

    function fetchData() {
        fetch('/getLastReadings')
            .then(response => response.json())
            .then(data => {
                if (data.timestamp == null) throw new Error("Error fetching data");
                console.log("Fetched data: ", data);

                for (let key in dataHistory) {
                    if (dataHistory.hasOwnProperty(key)) {
                        dataHistory[key].push(data[key]);
                        dataHistory[key].splice(0, dataHistory[key].length - 60);
                    }
                }

                updateLineChart(dataHistory);
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

    fetchData();
    setInterval(fetchData, 500);
});
