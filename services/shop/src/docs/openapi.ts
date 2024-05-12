import express, { Router } from 'express';
import { OpenApiGeneratorV3, OpenAPIRegistry } from "@asteasolutions/zod-to-openapi";
import swaggerUi from 'swagger-ui-express';

import { healthRegistry } from '../routes/health';

const generateSwagger = () => {
    const registry = new OpenAPIRegistry([healthRegistry]);
    const generator = new OpenApiGeneratorV3(registry.definitions);

    return generator.generateDocument({
        openapi: '3.0.0',
        info: {
            title: 'Shop API',
            version: '1.0.0'
        },
        externalDocs: {
            description: 'API Documentation for Shop Service',
            url: '/swagger.json',
        },
    })
}

export const openAPIRouter: Router = (() => {
    const router = express.Router();
    const swagger = generateSwagger();

    router.get('/swagger.json', (req, res) => {
        res.setHeader('Content-Type', 'application/json');
        res.json(swagger);
    });

    router.use('/', swaggerUi.serve, swaggerUi.setup(swagger));
    return router;
})();
