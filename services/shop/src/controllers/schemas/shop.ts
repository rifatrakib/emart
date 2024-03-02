export interface Shop {
    id: string;
    shop_id: number;
    name: string;
    merchant_id: number;
    address: string | null;
    description: string | null;
    account_number: string;
    email: string;
    phone_number: string;
    website: string | null;
    metadata: any;
    created_at: Date;
    updated_at: Date | null;
}
