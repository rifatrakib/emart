import express, { json, urlencoded } from 'express';
import swaggerUi from 'swagger-ui-express';

import config from './config/env';

import { RegisterRoutes } from '../build/routes';
import * as swaggerConfig from '../build/swagger.json';

const app: express.Application = express();

app.use(
    urlencoded({
        extended: true,
    })
);
app.use(json());

app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerConfig));

RegisterRoutes(app);

app.listen(config.PORT, () => {
    console.log(`Server is running on port ${config.PORT}`);
});
