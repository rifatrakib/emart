import express, { Router } from 'express';

import { createNewShop } from '../controllers/shop';
import { shopCreateRequest } from '../middlewares/shop';

export const shopRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.post('', shopCreateRequest, createNewShop);

    return router;
})();
