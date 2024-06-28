import { Request, Response } from 'express';
import { createShop, fetchShopById, fetchShops, fetchShopsByOwnerAccountId } from '../repositories/shop';
import { validator } from '../middlewares/validators';
import { ShopResponse } from '../models/schemas/responses/shop';

export const createNewShop = async (req: Request, res: Response) => {
    const ownerAccountId = (req.query.id as string) ? parseInt(req.query.id as string) : null;
    if (!ownerAccountId) {
        return res.status(400).json({ message: 'Owner account id is required' });
    }

    const newShop = await createShop(ownerAccountId, req.body);
    newShop.id = newShop._id?.toString();
    const result = await validator(ShopResponse, newShop);
    if (!result.isValid) {
        return res.status(422).json({ details: result.error?.details });
    }

    res.status(201).json({ message: 'Shop created', data: newShop });
}

export const readShops = async (req: Request, res: Response) => {
    const pageNumber = req.query.page ? parseInt(req.query.page as string) : 1;
    const term = req.query.q as string;

    const shops = await fetchShops(pageNumber, term);
    if (!shops.length) {
        return res.status(404).json({ message: 'Shops not found' });
    }

    shops.forEach(async shop => {
        const result = await validator(ShopResponse, shop);
        if (!result.isValid) {
            return res.status(422).json({ details: result.error?.details });
        }
    });

    res.status(200).json({ message: 'Shops found', data: shops });
};

export const readShopById = async (req: Request, res: Response) => {
    const shopId = req.params.id;
    if (!shopId) {
        return res.status(400).json({ message: 'Shop id is required' });
    }

    const shop = await fetchShopById(shopId);
    if (!shop) {
        return res.status(404).json({ message: 'Shop not found' });
    }

    shop.id = shop._id?.toString();
    const result = await validator(ShopResponse, shop);
    if (!result.isValid) {
        return res.status(422).json({ details: result.error?.details });
    }

    res.status(200).json({ message: 'Shop found', data: shop });
}

export const readShopsByOwnerAccountId = async (req: Request, res: Response) => {
    const ownerAccountId = req.params.id;
    const pageNumber = req.query.page ? parseInt(req.query.page as string) : 1;
    const sortDirection = req.query.sort ? req.query.sort as string : 'desc';

    if (!ownerAccountId) {
        return res.status(400).json({ message: 'Owner account id is required' });
    }

    const shops = await fetchShopsByOwnerAccountId(ownerAccountId, pageNumber, sortDirection);
    if (!shops.length) {
        return res.status(404).json({ message: 'Shops not found' });
    }

    shops.forEach(async shop => {
        const result = await validator(ShopResponse, shop);
        if (!result.isValid) {
            return res.status(422).json({ details: result.error?.details });
        }
    });

    res.status(200).json({ message: 'Shops found', data: shops });
}
