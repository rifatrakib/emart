import { Shop } from "../models/database/shop";

export const createShop = async (ownerAccountId: number, payload: object) => {
    const newShop = new Shop({ ...payload, ownerAccountId });
    await newShop.save();
    return newShop;
};

export const fetchShopById = async (shopId: string) => {
    return await Shop.findById(shopId);
};

export const fetchShopsByOwnerAccountId = async (ownerAccountId: string) => {
    return await Shop.find({ ownerAccountId });
}
