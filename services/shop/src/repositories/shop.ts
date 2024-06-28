import { appConfig } from '../config/parse';
import { Shop } from '../models/database/shop';

export const createShop = async (ownerAccountId: number, payload: object) => {
    const newShop = new Shop({ ...payload, ownerAccountId });
    await newShop.save();
    return newShop;
};

export const fetchShops = async (page: number, term: string) => {
    return await Shop.find({ $text: { $search: `\"${term}\"` } })
        .sort({ textScore: { $meta: 'textScore' }})
        .skip((page - 1) * appConfig.pageSize)
        .limit(appConfig.pageSize);
};

export const fetchShopById = async (shopId: string) => {
    return await Shop.findById(shopId);
};

export const fetchShopsByOwnerAccountId = async (ownerAccountId: string, page: number, sortDirection: string) => {
    const direction = sortDirection === 'asc' ? 1 : -1;
    return await Shop.find({ ownerAccountId })
        .skip((page - 1) * appConfig.pageSize)
        .limit(appConfig.pageSize)
        .sort({ createdAt: direction });
}
