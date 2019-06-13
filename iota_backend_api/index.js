const dotenv = require("dotenv");
dotenv.config();

const express = require("express");
const app = express();
const iota_helper = require("./iota_helpers");

app.get("/api/messages", async (req, res) => {
    const root = req.query.root;
    const key = req.query.key;
    const messagesResponse = await iota_helper.getMessages(root, key);
    res.json({
        success: true,
        messages: messagesResponse.messages,
        last_root: messagesResponse.last_root
    });
});

app.get("/api/root", (req, res) => {
    const seed = req.query.seed;
    const key = req.query.key;
    console.log(seed, key, req.query);
    const rootResponse = iota_helper.getRoot({
        seed,
        key
    });
    res.json({
        success: true,
        root: rootResponse.root,
        key_trytes: rootResponse.keyTrytes
    });
});

app.listen(3000 || process.env.PORT);
