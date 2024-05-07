import express, { Application, Request, Response } from 'express';
import cors from 'cors';

import { AppConfig } from './interfaces/config';
import { parseConfig } from './config/parse';

const app: Application = express();

const appConfig: AppConfig = parseConfig();

app.use(cors(appConfig.corsOptions));

app.get('/home', (req: Request, res: Response) => {
    res.send('<p>Hello World!</p>');
});

app.listen(appConfig.port, () => {
    console.log(`Server running on port ${appConfig.port}`);
});
