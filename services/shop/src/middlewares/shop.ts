import { Request, Response, NextFunction } from 'express';

import { validator } from '../middlewares/validators';
import { ShopCreateRequest, ShopUpdateRequest } from '../models/schemas/requests/shop';

export const shopCreateRequest = async (req: Request, res: Response, next: NextFunction) => {
    const result = await validator(ShopCreateRequest, req.body);
    if (!result.isValid) {
        return res.status(422).json({ details: result.error?.details });
    }
    next();
};

export const shopUpdateRequest = async (req: Request, res: Response, next: NextFunction) => {
    const result = await validator(ShopUpdateRequest, req.body);
    if (!result.isValid) {
        return res.status(422).json({ details: result.error?.details });
    }
    next();
};
