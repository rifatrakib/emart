export interface ShopCreateParams {
    name: string;
    merchant_id: number;
    address: string | null;
    description: string | null;
    account_number: string;
    email: string;
    phone_number: string;
    website: string | null;
    metadata: any;
}

export interface Shop {
    shop_id: number;
    name: string;
    merchant_id: number;
    address: string | null;
    description: string | null;
    email: string;
    phone_number: string;
    website: string | null;
    metadata: any;
}
