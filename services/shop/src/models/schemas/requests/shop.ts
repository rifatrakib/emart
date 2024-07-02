import Joi from 'joi';

import { validateTotalShares } from '../../../utils/validators';

const AddressSchema = Joi.object({
    street: Joi.string().required().max(256),
    city: Joi.string().required().max(256),
    state: Joi.string().max(256),
    country: Joi.string().required().max(256),
    postalCode: Joi.string().max(16),
});

const HeirSchema = Joi.object({
    accountId: Joi.number().required().min(1),
    share: Joi.number().required().min(0).max(1),
    explanation: Joi.string().optional().max(64),
    relationship: Joi.string().optional().max(64),
});

const OwnerSchema = Joi.object({
    accountId: Joi.number().required().min(1),
    share: Joi.number().required().min(0).max(1),
    explanation: Joi.string().optional().max(64),
    heirs: Joi.array().items(HeirSchema).custom(validateTotalShares),
});

export const ShopCreateRequest = Joi.object({
    name: Joi.string().required().max(256),
    registrationNumber: Joi.string().required(),
    address: AddressSchema.required(),
    logo: Joi.string().required(),
    description: Joi.string().max(1024),
    owners: Joi.array().items(OwnerSchema).required().custom(validateTotalShares),
    accountNumber: Joi.string().required().max(64),
    phoneNumber: Joi.string().required().max(16),
    email: Joi.string().email().required().max(256),
    additionalInformation: Joi.object(),
    metadata: Joi.object(),
});

export const ShopUpdateRequest = Joi.object({
    name: Joi.string().optional().max(256),
    registrationNumber: Joi.string().optional(),
    address: AddressSchema.optional(),
    logo: Joi.string().optional(),
    description: Joi.string().optional().max(1024),
    owners: Joi.array().items(OwnerSchema).optional().custom(validateTotalShares),
    accountNumber: Joi.string().optional().max(64),
    phoneNumber: Joi.string().optional().max(16),
    email: Joi.string().email().optional().max(256),
    additionalInformation: Joi.object().optional(),
    metadata: Joi.object().optional(),
});

export const UpdateInheritorsRequest = Joi.array().items(Joi.object({
    shopId: Joi.string().required().min(24).max(24),
    heirs: Joi.array().items(HeirSchema).required().custom(validateTotalShares),
}));
