$(document).ready(function () {
    setupRealtimeLineChart();

    async function fetchData() {
        try {
            const response = await fetch('/getLastReadings');
            const data = await response.json();
            updateRealtimeLineChart(data);
            $('#syncingModal').modal('hide');
        } catch (error) {
            $('#syncingModal').modal('show');
        }
    }

    async function fetchInterpolatedData() {
        try {
            const response = await fetch('/getLastReadingsWithInterpolation');
            const data = await response.json();
            updateMatrixChart(data);
        } catch (error) {
            $('#syncingModal').modal('show');
        }
    }

    async function fetchHistoryData() {
        try {
            const response = await fetch('/getHistory?seconds=600');
            const data = await response.json();
            updateHistoryLineChart(data);
        } catch (error) {
            $('#syncingModal').modal('show');
        }
    }

    // async function fetchIrrigationData() {
    //     try {
    //         const response = await fetch('/getIrrigationData');
    //         const data = await response.json();
    //         updateIrrigationLineChart(data);
    //     } catch (error) {
    //         $('#syncingModal').modal('show');
    //     }
    // }

    async function fetchAllIrrigationData() {
        try {
            const response = await fetch('/getIrrigationHistoryData?seconds=600');
            const data = await response.json();
            setupIrrigationLineChart(data);
        } catch (error) {
            $('#syncingModal').modal('show');
        }
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
        updateOptimalIrrigationLine(value);
    });

    $('#irrigationSlider').on('input', function () {
        var value = $(this).val();
        $('#sliderValue').text(value);
    });

    fetchData();
    //  fetchHistoryData();
    fetchInterpolatedData();
    fetchAllIrrigationData();
    setInterval(fetchData, 1000);
    setInterval(fetchInterpolatedData, 500);
});
