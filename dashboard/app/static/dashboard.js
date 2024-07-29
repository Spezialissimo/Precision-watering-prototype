
$(document).ready(function () {

    class PumpMode {
        static Manual = new PumpMode('Manual');
        static Auto = new PumpMode('Auto');

        constructor(name) {
            this.name = name;
        }
        toString() {
            return `PumpMode.${this.name}`;
        }
    }

    class PumpStatus {
        static On = new PumpStatus('On');
        static Off = new PumpStatus('Off');

        constructor(name) {
            this.name = name;
        }

        toString() {
            return `PumpStatus.${this.name}`;
        }
    }

    let pumpMode = PumpMode.Manual;
    let selectedOptimal = Optimals.Disabled;
    upsertIrrigationControls(selectedOptimal);

    async function fetchData() {
        try {
            const response = await fetch('/getLastReadings');
            const data = await response.json();
            setupRealtimeLineChart(data);
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
            $('#syncingModal').modal('hide');
        } catch (error) {
            $('#syncingModal').modal('show');
        }
    }

    async function fetchAllIrrigationData() {
        try {
            const response = await fetch('/getIrrigationHistoryData?seconds=600');
            const data = await response.json();
            setupIrrigationLineChart(data);
            $('#syncingModal').modal('hide');
        } catch (error) {
            $('#syncingModal').modal('show');
        }
    }

    $('#togglePump').click(function () {
        fetch('/togglePump');
    });

    $('#irrigationSlider').on('change', function () {
        var value = $(this).val();
        fetch('/setIrrigationPercentage?value=' + value, { method: 'POST' });
        updateOptimalIrrigationLine(value);
    });

    $('#irrigationSlider').on('input', function () {
        var value = $(this).val();
        $('#sliderValue').text(value);
    });

    $('#toggleMode').click(function () {
        if (pumpMode == PumpMode.Manual) {
            pumpMode = PumpMode.Auto;
            $('#togglePump').prop('disabled', true);
            $('#chooseOptimal').prop('disabled', false);
            $('#pumpMode').text('Automatic');
            selectedOptimal = Optimals.Slider;
            upsertIrrigationControls(selectedOptimal);
        } else {
            pumpMode = PumpMode.Manual;
            $('#togglePump').prop('disabled', false);
            $('#chooseOptimal').prop('disabled', true);
            $('#pumpMode').text('Manual');
            selectedOptimal = Optimals.Disabled;
            upsertIrrigationControls(selectedOptimal);
        }
    });

    $('#chooseOptimal').click(function () {
        $('#optimalSelectionModal').modal('show');
    });

    $('#sliderContainer').append(Optimals.Slider.toHtml());
    $('#matrix1Container').append(Optimals.Matrix1.toHtml());
    $('#matrix2Container').append(Optimals.Matrix2.toHtml());

    $('.card').click( function (e) {
        target = e.currentTarget;

        if (target.id.startsWith('slider')) {
            selectedOptimal = Optimals.Slider;
        } else if (target.id.startsWith('matrix1')) {
            selectedOptimal = Optimals.Matrix1;
        } else if (target.id.startsWith('matrix2')) {
            selectedOptimal = Optimals.Matrix2;
        }

        Optimals.foreach(o => $('#' + o.name + 'Card').removeClass('border-primary').removeClass('border-secondary'));
        $('#' + selectedOptimal.name + 'Card').addClass('border-primary');

        upsertIrrigationControls(selectedOptimal);

        if (selectedOptimal == Optimals.Slider) {
            // if not set in the past, get last optimal value from backend
        } else{
            fetch('/setIrrigationOptimalMatrix?file=' + selectedOptimal.value_uri, { method: 'POST' })
        }

    })

    $('.card').hover( function (e) {
        target = $("#" + e.currentTarget.id);
        if (!target.hasClass('border-primary')) {
            target.addClass('border-secondary');
        }
    })

    $('.card').on('mouseleave', function (e) {
        target = $("#" + e.currentTarget.id);
        if(target.hasClass('border-secondary')) {
            target.removeClass('border-secondary');
        }
    })

    fetchData();
    fetchInterpolatedData();
    fetchAllIrrigationData();
    setInterval(fetchInterpolatedData, 500);
});
