import { z } from 'zod';

export const healthResponseSchema = (schema: z.ZodTypeAny, description: string, statusCode = 200) => {
    const responseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
        z.object({
            status: z.string(),
        });

    return {
        [statusCode]: {
            description,
            content: {
                'application/json': {
                    schema: responseSchema(schema),
                },
            },
        },
    };
}
