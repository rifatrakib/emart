import Joi from 'joi';

export const ShopCreateRequest = Joi.object({
    name: Joi.string().required(),
    registrationNumber: Joi.string().required(),
    address: Joi.object({
        street: Joi.string().required(),
        city: Joi.string().required(),
        state: Joi.string(),
        country: Joi.string().required(),
        postalCode: Joi.string(),
    }).required(),
    logo: Joi.string().required(),
    description: Joi.string(),
    accountNumber: Joi.string().required(),
    phoneNumber: Joi.string().required(),
    email: Joi.string().email().required(),
    additionalInformation: Joi.object(),
    metadata: Joi.object(),
});
