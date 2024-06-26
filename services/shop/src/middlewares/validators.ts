import Joi from 'joi';

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
