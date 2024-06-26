import { Request, Response } from 'express';

export const createNewShop = async (req: Request, res: Response) => {
    res.status(201).json({ message: 'Shop created', shopData: req.body });
}
