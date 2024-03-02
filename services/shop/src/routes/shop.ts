import { Body, Controller, Post, Route } from 'tsoa';
import { Shop } from '../controllers/schemas/shop';
import { ShopCreateParams, ShopService } from '../controllers/services/shop';

@Route('shops')
export class ShopController extends Controller {
    @Post()
    public async createShop(
        @Body() body: ShopCreateParams
    ): Promise<Shop> {
        return await new ShopService().create(body);
    }
}
