import { ResponseSchema } from '../interfaces/base';

export const handle200Response = (body: any): ResponseSchema => {
    return {
        statusCode: 200,
        success: true,
        body,
    };
};
