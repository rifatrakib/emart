import { z } from 'zod';

export const healthSchema = z.object({
    status: z.string(),
    port: z.number(),
    app: z.string(),
});
