import express, { Request, Response } from 'express';

const app = express();
const PORT = 3000;

app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'OK' });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
