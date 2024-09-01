let timestampDelta = null;
function correctTimestamp(timestamp) {
    if(timestampDelta === null) {
        timestampDelta = (Date.now()/1000 - timestamp);
    }
    return timestamp + timestampDelta;
}

function convertTimestampToDateForRealtime(timestamp) {
    return (parseFloat(timestamp) * 1000);
}

function getBackgroundColor(value) {
    var valueInRange = value;

    let startColor, endColor;
    if (valueInRange <= 50) {
        startColor = { r: 215, g: 48, b: 39 };
        endColor = { r: 241, g: 163, b: 133 };
        valueInRange = valueInRange * 2;
    } else {
        startColor = { r: 241, g: 163, b: 133 };
        endColor = { r: 69, g: 117, b: 180 };
        valueInRange = (valueInRange - 50) * 2;
    }

    const r = startColor.r + (endColor.r - startColor.r) * (valueInRange / 100);
    const g = startColor.g + (endColor.g - startColor.g) * (valueInRange / 100);
    const b = startColor.b + (endColor.b - startColor.b) * (valueInRange / 100);

    return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
}


function putMoistureValueInRange(value) {
    return Math.max(Math.min(Math.round(((value - minMoisture)/(maxMoisture - minMoisture)) * 100), 100), 0);
}

function updateSliderValue(value) {
    lastSliderValue = value;
    var deNormValue = (value / 100) * (maxMoisture - minMoisture) + minMoisture;
    fetch('/irrigation/slider?value=' + deNormValue, { method: 'POST' });
    updateOptimalIrrigationLine(value);
}

function updateMatrixValues(matrix) {
    let copy = []
    matrix.forEach(element => {
        copy.push({
            'x': element.x,
            'y': element.y,
            'v': (element.v / 100) * (maxMoisture - minMoisture) + minMoisture
        })
    });
    fetch('/irrigation/matrix', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        body: JSON.stringify({ matrix: copy })
        })
        .then(response => response.json())
        .then(data => {
            updateOptimalIrrigationLine(data);
        });
}