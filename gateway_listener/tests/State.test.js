const State = require("../core/State");
const fs = require("fs");
const path = require("path");

test("getData returns data", () => {
    const s = new State("tmp", __dirname);
    const data = { one: 1 };
    s.setData(data);
    expect(JSON.stringify(data)).toBe(JSON.stringify(s.getData()));
});

test("setData writes state to file", () => {
    const root = __dirname;
    const name = "tmp2";
    const s = new State(name, root);
    const data = { one: 1 };
    s.setData(data);
    const content = fs.readFileSync(path.join(root, `state_${name}.json`)).toString();
    expect(content).toBe(JSON.stringify(data));
});
