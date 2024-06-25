import { ShopCreateRequest } from '../models/schemas/requests/shop';

export const validateShopCreateRequest = (shopData: Record<string, any>) => {
    const body = ShopCreateRequest.validate(shopData);
    return body;
};
