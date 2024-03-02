import { PrismaClient } from '@prisma/client';

import { Test } from '../schemas/test';

export type TestCreateParams = Pick<Test, 'title' | 'body'>;

export class TestService {
    public async create(params: TestCreateParams): Promise<Test> {
        const prisma = new PrismaClient();

        try {
            const newRecord = await prisma.test.create({
                data: {
                    title: params.title,
                    body: params.body,
                },
            });
            return {
                id: newRecord.id,
                title: newRecord.title,
                body: newRecord.body,
            };
        } catch (error: any) {
            throw new Error(`Error creating test: ${error}`);
        } finally {
            await prisma.$disconnect();
        }
    }
}
