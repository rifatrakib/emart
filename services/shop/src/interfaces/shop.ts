import { Document } from 'mongoose';

interface Address {
    street: string;
    city: string;
    state?: string;
    country: string;
    postalCode?: string;
}

export interface IShop extends Document {
    name: string;
    registrationNumber: string;
    address: Address;
    logo: string;
    description?: string;
    accountNumber: string;
    phoneNumber: string;
    email: string;
    otherContacts?: Record<string, any>;
    additionalInformation?: Record<string, any>;
    createdAt: Date;
    lastUpdatedAt: Date;
}
