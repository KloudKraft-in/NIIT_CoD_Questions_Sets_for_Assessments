const express = require('express');
const EventEmitter = require('events');
const app = express();

const globalEmitter = new EventEmitter();
globalEmitter.setMaxListeners(50);

app.get('/api/listen', (req, res) => {
    // LEAK: appends a new listener on every request.
    // TODO: Refactor this to use once() or remove the listener when the connection closes.
    globalEmitter.on('update', () => {
        console.log('Update received');
    });
    res.json({ registered: true });
});

module.exports = app;
