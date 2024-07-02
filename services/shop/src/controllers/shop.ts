import { Request, Response } from 'express';
import { createShop, fetchShops, fetchShopById, updateShop, deleteShop, transferShop, transferAllShops, transferMultipleShops, updateInheritors } from '../repositories/shop';

export const createNewShop = async (req: Request, res: Response) => {
    const newShop = await createShop(req.body);
    res.status(201).json({ message: 'Shop created', data: newShop });
};

export const readShops = async (req: Request, res: Response) => {
    const term = req.query.q ? req.query.q as string : null;
    const city = req.query.city ? req.query.city as string: null;
    const country = req.query.country ? req.query.country as string: null;
    const id = req.query.id ? parseInt(req.query.id as string) : null;
    const pageNumber = req.query.page ? parseInt(req.query.page as string) : 1;
    const demo = req.query.demo ? req.query.demo as string[] : null;
    console.log(demo);

    const shops = await fetchShops(term, country, city, id, pageNumber);
    if (!shops.length) {
        return res.status(404).json({ message: 'Shops not found' });
    }

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

    res.status(200).json({ message: 'Shop found', data: shop });
};

export const updateSingleShop = async (req: Request, res: Response) => {
    const shopId = req.params.id;
    if (!shopId) {
        return res.status(400).json({ message: 'Shop id is required' });
    }

    const updatedShop = await updateShop(shopId, req.body);
    if (!updatedShop) {
        return res.status(404).json({ message: 'Shop not found' });
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

export const updateInheritance = async (req: Request, res: Response) => {
    const ownerAccountId = parseInt(req.query.ownerAccountId as string);
    if (!ownerAccountId) {
        return res.status(400).json({ message: 'Shop owner account id is required' });
    }

    const updatedShopsCount = await updateInheritors(ownerAccountId, req.body);
    if (!updatedShopsCount) {
        return res.status(404).json({ message: 'Shop not found' });
    }

    res.status(200).json({ message: `${updatedShopsCount} shop(s) updated`});
};
