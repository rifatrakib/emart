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

export const updateShop = async (shopId: string, payload: object) => {
    let data = { ...payload, lastUpdatedAt: new Date() };
    return await Shop.findByIdAndUpdate(shopId, data, { new: true });
}

export const deleteShop = async (shopId: string) => {
    return await Shop.findByIdAndDelete(shopId);
};

export const transferShop = async (shopId: string, ownerAccountId: number, newOwnerAccountId: number) => {
    console.log({ _id: shopId, ownerAccountId });
    return await Shop.findOneAndUpdate({ _id: shopId, ownerAccountId }, { ownerAccountId: newOwnerAccountId }, { new: true })
};

export const transferMultipleShops = async (ownerAccountId: number, payload: Array<{ shopId: string, ownerId: number }>) => {
    const ops = payload.map(shop => ({
        updateOne: {
            filter: { _id: shop.shopId, ownerAccountId: ownerAccountId },
            update: { $set: { ownerAccountId: shop.ownerId } },
        }
    }));
    const result = await Shop.bulkWrite(ops);
    return result.modifiedCount;
};

export const transferAllShops = async (ownerAccountId: number, newOwnerAccountId: number) => {
    return (await Shop.updateMany({ ownerAccountId }, { ownerAccountId: newOwnerAccountId })).modifiedCount;
};
