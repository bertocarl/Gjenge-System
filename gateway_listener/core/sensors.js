const mqtt_wrapper = require("./mqtt_wrapper");

let sensorData = {};

const handlers = {};

function init() {
    handlers[process.env.MQTT_SENSOR_TEMPERATURE] = temperatureHandler;
    handlers[process.env.MQTT_SENSOR_GPS] = gpsHandler;
    handlers[process.env.MQTT_SENSOR_GAS] = gasHandler;

    mqtt_wrapper.connect(
        [process.env.MQTT_SENSOR_TEMPERATURE, process.env.MQTT_SENSOR_GPS, process.env.MQTT_SENSOR_GAS],
        onSensorMessage
    );
}

function getData() {
    sensorData["time"] = Date.now();
    return sensorData;
}

function onSensorMessage(topic, message) {
    if (handlers[topic]) {
        handlers[topic](message);
    }
}

function temperatureHandler(message) {
    sensorData["temperature"] = parseFloat(message);
}

function gpsHandler(message) {
    const gps = message.split(";");
    sensorData["gps"] = gps[0] + "+" + gps[1];
}

function gasHandler(message) {
    sensorData["gas"] = parseFloat(message);
}

module.exports = {
    init,
    getData
};
