const dotenv = require("dotenv");
dotenv.config();

const iota_helpers = require("../iota_helpers");

const testRoot = "PUKAZMCWYKKHKOQZPEDRIXWDZUPRJYJNXLLWWZATCVEUZPZDHWBAUWILMQFDB9KGEEXDCTLTUVHRYRSUK";
const testSeed = "seed1";
const testSecret = "secret1";

test("should return right root", () => {
    const root = iota_helpers.getRoot({
        seed: testSeed,
        key: testSecret
    });

    expect(root.root).toBe(testRoot);
});

test("should return messages and last_root", async () => {
    const messagesData = await iota_helpers.getMessages(testRoot, testSecret);
    console.log("messagesData", messagesData.last_root);
    expect(messagesData.messages[0].value).toBe(0.4402586878551673);
    expect(messagesData.last_root).toBe("GVJBYFQONZQWWSJDYIGWYWYCGKWIDCQGLJUNY9CDCBQDYNHBQYRIXFBIGMBFGBCGNXCNZIUXCNAUIEFMD");
});
