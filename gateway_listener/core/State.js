const fs = require("fs");
const path = require("path");

function readState(name, root) {
    try {
        const content = fs.readFileSync(path.join(root, `state_${name}.json`));
        return JSON.parse(content);
    } catch (e) {
        console.error("readState error", e);
    }

    return {};
}

function writeState(name, root, data) {
    fs.writeFileSync(path.join(root, `state_${name}.json`), JSON.stringify(data));
}

class State {
    constructor(name, root) {
        this.name = name;
        this.root = root;
        this.data = readState(this.name, this.root);
    }

    getData() {
        return this.data;
    }

    setData(data) {
        this.data = data;
        writeState(this.name, this.root, this.data);
    }
}

module.exports = State;
