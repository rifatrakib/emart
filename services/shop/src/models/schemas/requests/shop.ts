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

export const ShopUpdateRequest = Joi.object({
    name: Joi.string().optional(),
    registrationNumber: Joi.string().optional(),
    address: Joi.object({
        street: Joi.string().optional(),
        city: Joi.string().optional(),
        state: Joi.string().optional(),
        country: Joi.string().optional(),
        postalCode: Joi.string().optional(),
    }).optional(),
    logo: Joi.string().optional(),
    description: Joi.string().optional(),
    accountNumber: Joi.string().optional(),
    phoneNumber: Joi.string().optional(),
    email: Joi.string().email().optional(),
    additionalInformation: Joi.object().optional(),
    metadata: Joi.object().optional(),
});

export const BulkShopsTransferRequest = Joi.array().items(Joi.object({
    shopId: Joi.string().required(),
    ownerId: Joi.number().required(),
}));
