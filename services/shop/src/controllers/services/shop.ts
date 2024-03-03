import { PrismaClient } from '@prisma/client';

import { Shop } from '../schemas/shop';

export type ShopCreateParams = Pick<Shop, 'name' | 'merchant_id' | 'address' | 'description' | 'account_number' | 'email' | 'phone_number' | 'website' | 'metadata'>;

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
                data: {
                    shop_id: nextId,
                    name: params.name,
                    merchant_id: params.merchant_id,
                    address: params.address,
                    description: params.description,
                    account_number: params.account_number,
                    email: params.email,
                    phone_number: params.phone_number,
                    website: params.website,
                    metadata: params.metadata,
                },
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
}
