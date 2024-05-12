import express, { Request, Response, Router } from 'express';
import { OpenAPIRegistry } from '@asteasolutions/zod-to-openapi';
import { z } from 'zod';

import { healthResponseSchema } from '../docs/schemas';
import { handle200Response } from '../utils/response';

export const healthRegistry = new OpenAPIRegistry();

export const healthRouter: Router = ((): Router => {
    const router: Router = express.Router();

    healthRegistry.registerPath({
        method: 'get',
        path: '/health',
        tags: ['Health Check'],
        responses: healthResponseSchema(z.null(), 'Health Check', 200),
    })

    router.get('', (req: Request, res: Response) => {
        let response = handle200Response({status: 'ok'});
        res.status(response.statusCode).json(response.body);
    });

    return router;
})();
