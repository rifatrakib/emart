import { Shop } from "../models/database/shop";

export const createShop = async (ownerAccountId: number, payload: object) => {
    const newShop = new Shop({ ...payload, ownerAccountId });
    await newShop.save();
    return newShop;
};
