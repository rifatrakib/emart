import express from 'express';
import config from './config/env';

import { healthCheck } from './routes/health';

const app: express.Application = express();

app.get('/health', healthCheck);

app.listen(config.PORT, () => {
    console.log(`Server is running on port ${config.PORT}`);
});
