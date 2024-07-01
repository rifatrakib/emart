import { Model, Schema } from 'mongoose';

import { mongoUri } from '../../config/parse';
import { IAddress, IInheritor, IShop } from '../../interfaces/shop';
import { getDbConnection } from '../../config/db';

const addressSchema = new Schema<IAddress>({
    street: { type: String, required: true, maxlength: 256 },
    city: { type: String, required: true, index: true, maxlength: 256 },
    state: { type: String, maxlength: 256 },
    country: { type: String, required: true, index: true, maxlength: 256 },
    postalCode: { type: String, maxlength: 16 },
}, { _id: false });

const inheritorSchema = new Schema<IInheritor>({
    accountId: { type: Number, required: true, min: 1 },
    share: { type: Number, required: true, min: 0, max: 1 },
    explanation: { type: String, maxLength: 64 },
}, { _id: false });

const shopSchema = new Schema<IShop>({
    name: { type: String, required: true, index: 'text', maxlength: 256 },
    registrationNumber: { type: String, required: true, unique: true },
    address: { type: addressSchema, required: true },
    logo: { type: String, required: true },
    description: { type: String, maxlength: 1024 },
    ownerAccountId: { type: Number, required: true, index: true, min: 1 },
    inheritors: { type: [inheritorSchema], required: true },
    accountNumber: { type: String, required: true, maxlength: 64 },
    phoneNumber: { type: String, required: true, maxlength: 16 },
    email: { type: String, required: true, maxlength: 256 },
    otherContacts: { type: Object },
    additionalInformation: { type: Object },
    createdAt: { type: Date, default: Date.now },
    lastUpdatedAt: { type: Date, default: Date.now },
});

const conn = getDbConnection(`${mongoUri}/EMartShops`);

export const Shop: Model<IShop> = conn.model('shops', shopSchema);
