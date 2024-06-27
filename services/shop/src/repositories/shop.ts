import { Shop } from "../models/database/shop";

export const createShop = async (payload: object) => {
    const newShop = new Shop(payload);
    await newShop.save();
    return newShop;
};
