import Joi from 'joi';

import { ShopCreateRequest } from '../requests/shop';

export const ShopResponse = ShopCreateRequest.keys({
    id: Joi.string().required(),
    ownerAccountId: Joi.number().required(),
});
