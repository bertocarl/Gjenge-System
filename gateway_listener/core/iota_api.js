const { asciiToTrytes } = require("@iota/converter");
const Mam = require("@iota/mam");
const sensors = require("./sensors");
const fake_gps = require("./fake_gps");

let state;
let backendState;

function init(inState, inBackendState) {
    state = inState;
    backendState = inBackendState;
    sensors.init();

    setTimeout(update, parseInt(process.env.IOTA_SEND_INTERVAL) * 1000);
}

async function update() {
    const backendData = backendState.getData();
    let data = state.getData();
    if (backendData["transportation_id"] === undefined) return;
    if (backendData.key === undefined || backendData.seed === undefined) {
        console.error("need key and seed");
        return;
    }

    if (data["transportation_id"] !== backendData["transportation_id"]) {
        data = {};
        data["transportation_id"] = backendData["transportation_id"];
    }

    const mapOptions = {};
    mapOptions.key = backendData.key;
    mapOptions.seed = backendData.seed;

    if (data.next_root !== undefined) {
        mapOptions.next_root = data.next_root;
        mapOptions.start = data.start;
    }

    let mamState = initMam(mapOptions);

    const payload = sensors.getData();
    if (fake_gps.isActive()) {
        let index = 0;
        if (mamState.channel && mamState.channel.start) {
            index = mamState.channel.start;
        }
        payload.gps = fake_gps.getData(index);

        if (payload.gps == null) {
            console.error("no gps data");
            return;
        }
    }

    mamState = await publish(mamState, payload);

    if (!mamState) {
        console.error("skip saving");
        setTimeout(update, parseInt(process.env.IOTA_SEND_INTERVAL) * 1000);
        return;
    }

    data.next_root = mamState.channel.next_root;
    data.start = mamState.channel.start;

    state.setData(data);

    setTimeout(update, parseInt(process.env.IOTA_SEND_INTERVAL) * 1000);
}

function initMam(options) {
    const secretKey = options.key;
    const senderSeed = options.seed;
    const mamMode = "restricted";

    console.log(options);

    let mamState = Mam.init(process.env.IOTA_PROVIDER, asciiToTrytes(senderSeed));
    mamState = Mam.changeMode(mamState, mamMode, asciiToTrytes(secretKey));

    if (options.next_root) {
        mamState.channel.next_root = options.next_root;
        mamState.channel.start = options.start;
    }

    return mamState;
}

async function publish(mamState, payload) {
    console.log("publish", payload);

    const trytes = asciiToTrytes(JSON.stringify(payload));
    const message = Mam.create(mamState, trytes);

    // Save new mamState
    mamState = message.state;

    // Attach the payload.
    try {
        console.time("attach");
        await Mam.attach(message.payload, message.address);
        console.timeEnd("attach");
        console.log("Root: ", message.root);
        console.log("Address: ", message.address);
    } catch (e) {
        console.log(e);
        return null;
    }

    return mamState;
}

module.exports = {
    init
};
