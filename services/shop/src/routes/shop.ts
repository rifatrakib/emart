import express, { Request, Response, Router } from 'express';

import { validateShopCreateRequest } from '../utils/requests';

export const shopRouter: Router = ((): Router => {
    const router: Router = express.Router();

    router.post('', (req: Request, res: Response) => {
        const shopData = validateShopCreateRequest(req.body);
        res.status(201).json({ message: 'Shop created', shopData });
    });

    return router;
})();
