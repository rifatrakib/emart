import { Document } from 'mongoose';

interface IAddress {
    street: string;
    city: string;
    state?: string;
    country: string;
    postalCode?: string;
}

interface IInheritor {
    accountId: number;
    share: number;
}

export interface IShop extends Document {
    name: string;
    registrationNumber: string;
    address: IAddress;
    logo: string;
    description?: string;
    ownerAccountId: number;
    inheritors: IInheritor[];
    accountNumber: string;
    phoneNumber: string;
    email: string;
    otherContacts?: Record<string, any>;
    additionalInformation?: Record<string, any>;
    createdAt: Date;
    lastUpdatedAt: Date;
}
