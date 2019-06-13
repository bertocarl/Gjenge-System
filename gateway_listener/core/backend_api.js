const axios = require("axios");

let currentState = null;

function init(state) {
    currentState = state;
    setInterval(update, 5 * 1000);
}

async function update() {
    const stateData = currentState.getData();

    const payload = {
        device_id: process.env.DEVICE_ID,
        transportation_id: stateData["transportation_id"],
        time: Date.now()
    };

    try {
        // TODO: add device signature to payload
        const response = await axios.post(process.env.BACKEND_URL, payload);

        // TODO: check signature from request
        if (response.data.success && response.data.state) {
            updateState(response.data.state);
        }
    } catch (e) {
        console.error("update request error", e);
    }
}

function updateState(newState) {
    const stateData = currentState.getData();

    if (newState["transportation_id"] !== undefined) {
        if (newState["transportation_id"] !== stateData["transportation_id"]) {
            currentState.setData(newState);
        }
    } else {
        currentState.setData({});
    }
}

module.exports = {
    init
};
