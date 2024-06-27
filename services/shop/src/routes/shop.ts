import express, { Router } from 'express';

import { createNewShop, readShopById } from '../controllers/shop';
import { shopCreateRequest } from '../middlewares/shop';

export const shopRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.post('', shopCreateRequest, createNewShop);
    router.get('/:id', readShopById);

    return router;
})();
