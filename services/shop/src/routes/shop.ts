import express, { Router } from 'express';

import { createNewShop, readShopById, readShops, readShopsByOwnerAccountId } from '../controllers/shop';
import { shopCreateRequest } from '../middlewares/shop';

export const shopRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.post('', shopCreateRequest, createNewShop);
    router.get('', readShops);
    router.get('/:id', readShopById);
    router.get('/owners/:id', readShopsByOwnerAccountId);

    return router;
})();
