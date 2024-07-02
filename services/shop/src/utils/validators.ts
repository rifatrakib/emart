import Joi from 'joi';

import { CustomHelpers, CustomValidator } from 'joi';
import { IHeir, IOwner } from '../interfaces/shop';

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

export const validateTotalShares: CustomValidator<IHeir[] | IOwner[]> = (persons: IHeir[] | IOwner[], helpers: CustomHelpers) => {
    const totalShare = persons.reduce((sum, person) => sum + person.share, 0);
    if (totalShare > 1) {
        return helpers.error('any.invalid', { message: 'Total share cannot exceed 1' });
    }
    return persons;
};
