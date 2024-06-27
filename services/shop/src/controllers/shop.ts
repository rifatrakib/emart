import { Request, Response } from 'express';
import { createShop } from '../repositories/shop';

export const createNewShop = async (req: Request, res: Response) => {
    const newShop = await createShop(req.body);
    res.status(201).json({ message: 'Shop created', data: newShop });
}
