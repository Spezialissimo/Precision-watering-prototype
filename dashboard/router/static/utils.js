function convertTimestampToDateForRealtime(timestamp) {
    return (parseFloat(timestamp) * 1000);
}

function convertToMatrixData(data) {
    return data["data"].map(obj => ({
        x: String(obj.x),
        y: String(obj.y),
        v: putMoistureValueInRange(Math.round(obj.v))
    }));
}

function getBackgroundColor(value) {
    const valueInRange = putMoistureValueInRange(value);
    const startColor = { r: 178, g: 34, b: 34 };
    const endColor = { r: 0, g: 0, b: 255 };
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