const mqtt = require("mqtt");

let client = null;

function connect(topics, onMessage) {
    if (client) {
        client.end();
    }

    client = mqtt.connect(process.env.MQTT_URL, {
        username: process.env.MQTT_USER,
        password: process.env.MQTT_PASSWORD,
        port: process.env.MQTT_PORT
    });

    client.on("connect", () => {
        console.log("connect");
        for (let topic of topics) {
            client.subscribe(topic, err => {
                if (err) {
                    console.error("subscribe error", err);
                } else {
                    console.log("subscribe to " + topic);
                }
            });
        }
    });

    if (onMessage) {
        client.on("message", (topic, message) => onMessage(topic, message.toString()));
    }
}

function disconnect() {
    if (client) {
        client.end();
    }
}

module.exports = {
    connect,
    disconnect
};
