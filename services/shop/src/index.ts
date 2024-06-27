import express, { Application } from 'express';
import cors from 'cors';

import { appConfig } from './config/parse';
import { initDb } from './events/startup';
import { healthRouter } from './routes/health';
import { shopRouter } from './routes/shop';

const startServer = async () => {
    const app: Application = express();

    app.use(cors(appConfig.corsOptions));
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));

    app.use('/health', healthRouter);
    app.use('/shops', shopRouter);

    await initDb();

    app.listen(appConfig.port, () => {
        console.log(`Server running on port ${appConfig.port}`);
    });
}

startServer();
