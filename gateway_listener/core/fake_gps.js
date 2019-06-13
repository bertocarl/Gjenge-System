const fs = require("fs");
let routeData;

function init(filepath) {
    routeData = JSON.parse(fs.readFileSync(filepath));
}

function getData(index) {
    let point;
    if (index < routeData.checkpoints.length) {
        point = routeData.checkpoints[index];
        return toGPSString(point);
    }

    return null;
}

function isActive() {
    return routeData !== undefined;
}

function toGPSString(point) {
    return point.lat + "+" + point.lng;
}

module.exports = {
    init,
    getData,
    isActive
};
