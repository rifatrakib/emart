import express, { Request, Response, Router } from 'express';

import { validateHealthResponse } from '../utils/responses';
import { AppConfig } from '../interfaces/config';
import { parseConfig } from '../config/parse';

export const healthRouter: Router = ((): Router => {
    const router: Router = express.Router();
    const appConfig: AppConfig = parseConfig();

    router.get('', (req: Request, res: Response) => {
        const result = validateHealthResponse({
            status: 'ok',
            port: appConfig.port,
            app: appConfig.app,
        });
        res.status(200).json(result);
    });

    return router;
})();
