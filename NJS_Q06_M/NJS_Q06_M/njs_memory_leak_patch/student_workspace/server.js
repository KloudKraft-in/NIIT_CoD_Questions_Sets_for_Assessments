const express = require('express');
const app = express();

// LEAK: Cache grows infinitely. Patch it to keep maximum 100 elements.
const cache = new Map();

app.get('/api/track', (req, res) => {
    const id = req.query.id || 'default';
    cache.set(id, { timestamp: Date.now(), metadata: req.headers });
    
    // TODO: Patch memory leak by ensuring cache size does not exceed 100 elements (evict oldest entries if size > 100)
    
    res.json({ tracked: true, cacheSize: cache.size });
});

module.exports = app;
