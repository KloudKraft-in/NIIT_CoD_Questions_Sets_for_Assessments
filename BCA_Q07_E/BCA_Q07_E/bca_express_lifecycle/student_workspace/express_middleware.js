const express = require('express');
const app = express();

const loggerMiddleware = (req, res, next) => {
  console.log('Request logged');
  next();
};

const authMiddleware = (req, res, next) => {
  res.status(401).send('Unauthorized');
};

app.use(loggerMiddleware);
app.use(authMiddleware);
