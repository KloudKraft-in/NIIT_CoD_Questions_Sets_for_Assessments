// server.js - Currently blocking event loop synchronously. Offload to worker.js using worker_threads!
const express = require('express');
const crypto = require('crypto');
const app = express();

app.get('/hash', (req, res) => {
    const password = req.query.password || 'secret';
    // TODO: Offload CPU-intensive hashing to worker.js using worker_threads Worker pool
    const hash = crypto.pbkdf2Sync(password, 'salt', 100000, 64, 'sha512').toString('hex');
    res.json({ hash });
});

module.exports = app;
