import { Body, Controller, Get, Post, Query, Route, SuccessResponse } from 'tsoa';
import { Shop, ShopCreateParams } from '../controllers/schemas/shop';
import { ShopService } from '../controllers/services/shop';

@Route('shops')
export class ShopController extends Controller {
    @SuccessResponse("201", "Created")
    @Post()
    public async createShop(
        @Body() body: ShopCreateParams,
    ): Promise<Shop> {
        return await new ShopService().create(body);
    }

    @Get()
    public async getShops(
        @Query() name?: string,
        @Query() merchantId?: number,
        @Query() page?: number,
    ): Promise<Shop[]> {
        return await new ShopService().readMany(name, merchantId, page);
    }

    @Get('{shopId}')
    public async getShop(
        shopId: number,
    ): Promise<Shop> {
        return await new ShopService().readOne(shopId);
    }
}
