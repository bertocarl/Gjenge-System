const { asciiToTrytes, trytesToAscii } = require("@iota/converter");
const Mam = require("@iota/mam");

async function getMessages(root, secretKey) {
    const secretKeyTrytes = asciiToTrytes(secretKey);
    const mamMode = "restricted";

    const mamState = Mam.init(process.env.IOTA_PROVIDER, undefined);
    Mam.changeMode(mamState, mamMode, secretKeyTrytes);

    let messages = [];

    const response = await Mam.fetch(root, mamMode, secretKeyTrytes, function(data) {
        let payload = trytesToAscii(data);
        messages.push(JSON.parse(payload));
    });

    return {
        last_root: response.nextRoot,
        messages
    };
}

function getRoot(options) {
    const secretKey = options.key;
    const secretKeyTrytes = asciiToTrytes(secretKey);
    const senderSeed = options.seed;
    const mamMode = "restricted";

    let mamState = Mam.init(process.env.IOTA_PROVIDER, asciiToTrytes(senderSeed));
    mamState = Mam.changeMode(mamState, mamMode, secretKeyTrytes);
    return {
        root: Mam.getRoot(mamState),
        keyTrytes: secretKeyTrytes
    };
}

module.exports = {
    getMessages,
    getRoot
};
