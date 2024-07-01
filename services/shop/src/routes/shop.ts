import express, { Router } from 'express';

import { renewInheritors, bulkTransferShops, createNewShop, deleteSingleShop, readShopById, readShops, transferAllOwnerShops, transferSingleShop, updateSingleShop } from '../controllers/shop';
import { bulkTransferShopsRequest, shopCreateRequest, shopUpdateRequest, updateInheritorsRequest } from '../middlewares/shop';

export const shopRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.post('', shopCreateRequest, createNewShop);

    router.get('', readShops);
    router.get('/:id', readShopById);

    router.patch('', bulkTransferShopsRequest, bulkTransferShops);
    router.patch('/transfer', transferAllOwnerShops);
    router.patch('/inheritors', updateInheritorsRequest, renewInheritors);
    router.patch('/:id/transfer', transferSingleShop);
    router.patch('/:id', shopUpdateRequest, updateSingleShop);

    router.delete('/:id', deleteSingleShop);

    return router;
})();
