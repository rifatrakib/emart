import { appConfig } from '../config/parse';
import { Shop } from '../models/database/shop';

export const createShop = async (ownerAccountId: number, payload: object) => {
    const newShop = new Shop({ ...payload, ownerAccountId });
    await newShop.save();
    return newShop;
};

export const fetchShops = async (term: string | null, country: string | null, city: string | null, ownerAccountId: number | null, page: number) => {
    let query = {};
    let sortQuery = {};

    if (term) {
        query = { $text: { $search: `\"${term}\"` } };
        sortQuery = { textScore: { $meta: 'textScore' }};
    } else {
        sortQuery = { createdAt: -1 };
    }

    if (country) {
        query = { ...query, 'address.country': country };
    }
    if (city) {
        query = { ...query, 'address.city': city };
    }
    if (ownerAccountId) {
        query = { ...query, ownerAccountId };
    }

    return await Shop.find(query)
        .sort(sortQuery)
        .skip((page - 1) * appConfig.pageSize)
        .limit(appConfig.pageSize);
};

export const fetchShopById = async (shopId: string) => {
    return await Shop.findById(shopId);
};
