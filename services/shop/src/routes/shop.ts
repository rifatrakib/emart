import express, { Router } from 'express';

import { createNewShop, readShopById, readShops, updateSingleShop } from '../controllers/shop';
import { shopCreateRequest, shopUpdateRequest } from '../middlewares/shop';

export const shopRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.post('', shopCreateRequest, createNewShop);
    router.get('', readShops);
    router.get('/:id', readShopById);
    router.patch('/:id', shopUpdateRequest, updateSingleShop);

    return router;
})();
