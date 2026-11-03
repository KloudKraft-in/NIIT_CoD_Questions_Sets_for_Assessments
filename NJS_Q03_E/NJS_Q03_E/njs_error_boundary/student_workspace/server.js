const express = require('express');
const app = express();

// TODO: Register global process exception listeners for uncaughtException and unhandledRejection

app.get('/error', (req, res) => {
    // TODO: Wrap async errors and route to Express error boundaries
    Promise.reject(new Error("Async Database Failure"));
});

// TODO: Add Express global error handling middleware

module.exports = app;
