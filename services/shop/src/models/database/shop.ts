import { Schema, Model } from 'mongoose';

import { mongoUri } from '../../config/parse';
import { IShop } from '../../interfaces/shop';
import { getDbConnection } from '../../config/db';

const shopSchema = new Schema<IShop>({
    name: { type: String, required: true },
    registrationNumber: { type: String, required: true },
    address: { type: Object, required: true },
    logo: { type: String, required: true },
    description: { type: String },
    ownerAccountId: { type: Number, required: true },
    accountNumber: { type: String, required: true },
    phoneNumber: { type: String, required: true },
    email: { type: String, required: true },
    otherContacts: { type: Object },
    additionalInformation: { type: Object },
    createdAt: { type: Date, default: Date.now },
    lastUpdatedAt: { type: Date, default: Date.now },
});
shopSchema.index({ name: 'text' });
shopSchema.index({ ownerAccountId: 1 });
shopSchema.index({ 'address.city': 1 });
shopSchema.index({ 'address.country': 1 });

const conn = getDbConnection(`${mongoUri}/EMartShops`);

export const Shop: Model<IShop> = conn.model('shops', shopSchema);
