import express, { Application } from 'express';
import cors from 'cors';

import { AppConfig } from './interfaces/config';
import { parseConfig } from './config/parse';
import { healthRouter } from './routes/health';
import { shopRouter } from './routes/shop';

const app: Application = express();

const appConfig: AppConfig = parseConfig();

app.use(cors(appConfig.corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/health', healthRouter);
app.use('/shops', shopRouter);

app.listen(appConfig.port, () => {
    console.log(`Server running on port ${appConfig.port}`);
});
