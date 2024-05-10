import express, { Request, Response, Router } from 'express';

export const healthRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.get('', (req: Request, res: Response) => {
        res.send({'status': 'ok'});
    });

    return router;
})();
