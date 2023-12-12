import express from 'express';
import { logger } from './logger.js';

const app = express();
app.use(logger);

app.get('/shop-api/health', (req, res) => {
    res.status(200).json({ status: 'ok' });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
