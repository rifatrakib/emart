import { Request, Response } from 'express';
import { createShop } from '../repositories/shop';
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
        return res.status(400).json({ details: result.error?.details });
    }

    res.status(201).json({ message: 'Shop created', data: newShop });
}
