import express, { Router } from 'express';

import { healthController } from '../controllers/health';

export const healthRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.get('', healthController);

    return router;
})();
