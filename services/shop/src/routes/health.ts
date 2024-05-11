import express, { Request, Response, Router } from 'express';

import { handle200Response } from '../utils/response';

export const healthRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.get('', (req: Request, res: Response) => {
        let response = handle200Response({status: 'ok'});
        res.status(response.statusCode).json(response.body);
    });

    return router;
})();
