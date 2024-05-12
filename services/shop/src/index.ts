import express, { Application } from 'express';
import cors from 'cors';

import { AppConfig } from './interfaces/config';
import { parseConfig } from './config/parse';
import { openAPIRouter } from './docs/openapi';
import { healthRouter } from './routes/health';

const app: Application = express();

const appConfig: AppConfig = parseConfig();

app.use(cors(appConfig.corsOptions));

app.use('/health', healthRouter);
app.use('/docs', openAPIRouter);

app.listen(appConfig.port, () => {
    console.log(`Server running on port ${appConfig.port}`);
});
