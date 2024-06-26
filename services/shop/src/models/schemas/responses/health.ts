import Joi from 'joi';

export const healthSchema = Joi.object({
    status: Joi.string().required(),
    port: Joi.number().required(),
    app: Joi.string().required(),
});
