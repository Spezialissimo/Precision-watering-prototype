function convertTimestampToDateForRealtime(timestamp) {
    return (parseFloat(timestamp) * 1000);
}

function convertToMatrixData(data) {
    return data["data"].map(obj => ({
        x: String(obj.x),
        y: String(obj.y),
        v: Math.round(obj.v)
    }));
}

function getBackgroundColor(value) {
    const startColor = { r: 178, g: 34, b: 34 };
    const endColor = { r: 0, g: 0, b: 255 };
    const r = startColor.r + (endColor.r - startColor.r) * (value / 100);
    const g = startColor.g + (endColor.g - startColor.g) * (value / 100);
    const b = startColor.b + (endColor.b - startColor.b) * (value / 100);
    return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
}

function putMoistureValueInRange(value) {
    if (value < minMoisture) {
        return minMoisture;
    }
    if (value > maxMoisture) {
        return maxMoisture;
    }
    return value;
}