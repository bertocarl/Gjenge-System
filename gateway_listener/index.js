const dotenv = require("dotenv");
dotenv.config();

const path = require("path");
const State = require("./core/State");
const backend_api = require("./core/backend_api");
const iota_api = require("./core/iota_api");
const fake_gps = require("./core/fake_gps");

const backendState = new State("backend", __dirname);
const iotaState = new State("iota", __dirname);

if (process.env.FAKE_GPS) {
    fake_gps.init(path.join(__dirname, "fake_data", process.env.FAKE_GPS));
}

backend_api.init(backendState);
iota_api.init(iotaState, backendState);
