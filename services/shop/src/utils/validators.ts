import Joi from 'joi';

import { CustomHelpers, CustomValidator } from 'joi';
import { IInheritor } from '../interfaces/shop';

export const validator = async (schema: Joi.ObjectSchema, body: object) => {
    const payload = await schema.validate(body, {
        abortEarly: false,
        allowUnknown: true,
        stripUnknown: true,
    });

    if (payload.error) {
        return { error: payload.error, isValid: false };
        }
    return { isValid: true, value: payload.value };
};

export const arrayValidator = async (schema: Joi.ArraySchema, body: Array<object>) => {
    const payload = await schema.validate(body, {
        abortEarly: false,
        allowUnknown: true,
        stripUnknown: true,
    });

    if (payload.error) {
        return { error: payload.error, isValid: false };
    }
    return { isValid: true, value: payload.value };
};

export const validateTotalShares: CustomValidator<IInheritor[]> = (inheritors: IInheritor[], helpers: CustomHelpers) => {
    const totalShare = inheritors.reduce((sum, inheritor) => sum + inheritor.share, 0);
    if (totalShare > 1) {
        return helpers.error('any.invalid', { message: 'Total share of inheritors cannot exceed 1' });
    }
    return inheritors;
};
