import { PrismaClient } from '@prisma/client';

import { Shop, ShopCreateParams, ShopUpdateParams } from '../schemas/shop';

export class ShopService {
    public async create(params: ShopCreateParams): Promise<Shop> {
        const prisma = new PrismaClient();

        try {
            const lastShop = await prisma.sequences.findUnique({
                where: { collection: 'shops' },
            });

            let nextId = 1;
            if (!lastShop) {
                await prisma.sequences.create({
                    data: {
                        collection: 'shops',
                        last_id: 1,
                    },
                });
            } else {
                nextId = lastShop.last_id + 1;
            }

            const newRecord = await prisma.shops.create({
                data: { ...params, shop_id: nextId },
            });

            await prisma.sequences.update({
                where: { collection: 'shops' },
                data: { last_id: nextId, updated_at: new Date()},
            });
            return newRecord as Shop;
        } catch (error: any) {
            throw new Error(`Error creating shop: ${error}`);
        } finally {
            await prisma.$disconnect();
        }
    }

    public async readMany(name?: string, merchantId?: number, page?: number): Promise<Shop[]> {
        const prisma = new PrismaClient();

        try {
            let query = {};
            if (name) {
                query = { ...query, name: name };
            }
            if (merchantId) {
                query = { ...query, merchant_id: merchantId };
            }

            const records = await prisma.shops.findMany({
                where: query,
                skip: page ? (page - 1) * 10 : 0,
                take: 10,
            });

            return records as Shop[];
        } catch (error: any) {
            throw new Error(`Error reading shops: ${error}`);
        } finally {
            await prisma.$disconnect();
        }
    }

    public async readOne(shopId: number) {
        const prisma = new PrismaClient();

        try {
            const record = await prisma.shops.findUnique({
                where: { shop_id: shopId },
            });

            return record as Shop;
        } catch (error: any) {
            throw new Error(`Error reading shop: ${error}`);
        } finally {
            await prisma.$disconnect();
        }
    }

    public async updateOne(shopId: number, data: ShopUpdateParams) {
        const prisma = new PrismaClient();
        let updateData: Record<string, any> = {};
        data.set_fields.forEach((field) => {
            if (field in data) {
                updateData[field] = data[field as keyof ShopUpdateParams];
            }
        });

        try {
            const record = await prisma.shops.update({
                where: { shop_id: shopId },
                data: { ...updateData, updated_at: new Date()},
            });

            return record as Shop;
        } catch (error: any) {
            throw new Error(`Error updating shop: ${error}`);
        } finally {
            await prisma.$disconnect();
        }
    }
}
