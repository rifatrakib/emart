import { z } from 'zod';

import { healthSchema } from '../models/schemas/health';

export const validateHealthResponse = (data: object) => {
    type HealthResponse = z.infer<typeof healthSchema>;
    return healthSchema.parse(data) as HealthResponse;
};
