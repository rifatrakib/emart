import { Request, Response } from 'express';
import { createShop, fetchShops, fetchShopById, updateShop, deleteShop, transferShop, transferAllShops, transferMultipleShops } from '../repositories/shop';
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
};

export const readShops = async (req: Request, res: Response) => {
    const term = req.query.q ? req.query.q as string : null;
    const city = req.query.city ? req.query.city as string: null;
    const country = req.query.country ? req.query.country as string: null;
    const ownerAccountId = req.query.id ? parseInt(req.query.id as string) : null;
    const pageNumber = req.query.page ? parseInt(req.query.page as string) : 1;

    const shops = await fetchShops(term, country, city, ownerAccountId, pageNumber);
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
};

export const updateSingleShop = async (req: Request, res: Response) => {
    const shopId = req.params.id;
    if (!shopId) {
        return res.status(400).json({ message: 'Shop id is required' });
    }

    console.log(req.body);
    const updatedShop = await updateShop(shopId, req.body);
    if (!updatedShop) {
        return res.status(404).json({ message: 'Shop not found' });
    }

    updatedShop.id = updatedShop._id?.toString();
    const result = await validator(ShopResponse, updatedShop);
    if (!result.isValid) {
        return res.status(422).json({ details: result.error?.details });
    }

    res.status(200).json({ message: 'Shop updated', data: updatedShop });
};

export const deleteSingleShop = async (req: Request, res: Response) => {
    const shopId = req.params.id;
    if (!shopId) {
        return res.status(400).json({ message: 'Shop id is required' });
    }

    const deletedShop = await deleteShop(shopId);
    if (!deletedShop) {
        return res.status(404).json({ message: 'Shop not found' });
    }

    res.status(204).send();
};

export const transferSingleShop = async (req: Request, res: Response) => {
    const shopId = req.params.id;
    const ownerAccountId = parseInt(req.query.ownerAccountId as string);
    if (!ownerAccountId) {
        return res.status(400).json({ message: 'Shop owner account id is required' });
    }

    const newOwnerAccountId = parseInt(req.query.newOwnerAccountId as string);
    if (!newOwnerAccountId) {
        return res.status(400).json({ message: 'New owner account id is required' });
    }

    const updatedShop = await transferShop(shopId, ownerAccountId, newOwnerAccountId);
    if (!updatedShop) {
        return res.status(404).json({ message: 'Shop not found' });
    }

    updatedShop.id = updatedShop._id?.toString();
    const result = await validator(ShopResponse, updatedShop);
    if (!result.isValid) {
        return res.status(422).json({ details: result.error?.details });
    }

    res.status(200).json({ message: 'Shop transferred', data: updatedShop });
};

export const bulkTransferShops = async (req: Request, res: Response) => {
    const ownerAccountId = parseInt(req.query.ownerAccountId as string);
    if (!ownerAccountId) {
        return res.status(400).json({ message: 'Shop owner account id is required' });
    }

    const updatedShopsCount = await transferMultipleShops(ownerAccountId, req.body);
    if (!updatedShopsCount) {
        return res.status(404).json({ message: 'Shops not found' });
    }

    res.status(200).json({ message: `${updatedShopsCount} shop(s) transferred` });
};

export const transferAllOwnerShops = async (req: Request, res: Response) => {
    const ownerAccountId = parseInt(req.query.ownerAccountId as string);
    if (!ownerAccountId) {
        return res.status(400).json({ message: 'Shop owner account id is required' });
    }

    const newOwnerAccountId = parseInt(req.query.newOwnerAccountId as string);
    if (!newOwnerAccountId) {
        return res.status(400).json({ message: 'New owner account id is required' });
    }

    const updatedShopsCount = await transferAllShops(ownerAccountId, newOwnerAccountId);
    if (!updatedShopsCount) {
        return res.status(404).json({ message: 'Shops not found' });
    }

    res.status(200).json({ message: `${updatedShopsCount} shop(s) transferred` });
};
