import express from 'express';

const app = express();

app.get('/shop-api/health', (req, res) => {
    res.json({ status: 'ok' });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
