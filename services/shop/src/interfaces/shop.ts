import { Document } from 'mongoose';

export interface IAddress {
    street: string;
    city: string;
    state?: string;
    country: string;
    postalCode?: string;
}

export interface IHeir {
    accountId: number;
    share: number;
    explanation?: string;
    relationship?: string;
}

export interface IOwner {
    accountId: number;
    share: number;
    explanation?: string;
    heirs?: IHeir[];
}

export interface IShop extends Document {
    name: string;
    registrationNumber: string;
    address: IAddress;
    logo: string;
    description?: string;
    owners: IOwner[];
    accountNumber: string;
    phoneNumber: string;
    email: string;
    otherContacts?: Record<string, any>;
    additionalInformation?: Record<string, any>;
    createdAt: Date;
    lastUpdatedAt: Date;
}
