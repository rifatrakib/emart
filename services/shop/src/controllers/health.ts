import { Request, Response } from 'express';

import { appConfig } from '../config/parse';
import { validator } from '../middlewares/validators';
import { healthSchema } from '../models/schemas/responses/health';

export const healthController = async (req: Request, res: Response) => {
    const result = await validator(healthSchema, {
        status: 'ok',
        port: appConfig.port,
        app: appConfig.app,
    });
    if (!result.isValid) {
        return res.status(400).json({ details: result.error?.details });
    }
    res.status(200).json(result.value);
};
