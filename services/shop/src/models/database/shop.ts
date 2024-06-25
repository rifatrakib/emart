import { model, Schema, Model } from 'mongoose';

import { Shop } from '../../interfaces/shop';

const shopSchema = new Schema<Shop>({
    name: { type: String, required: true },
    registrationNumber: { type: String, required: true },
    address: { type: Object, required: true },
    logo: { type: String, required: true },
    description: { type: String },
    accountNumber: { type: String, required: true },
    phoneNumber: { type: String, required: true },
    email: { type: String, required: true },
    otherContacts: { type: Object },
    additionalInformation: { type: Object },
    createdAt: { type: Date, default: Date.now },
    lastUpdatedAt: { type: Date, default: Date.now },
});
shopSchema.index({ name: 'text', 'address.city': 1, 'address.country': 1 });

export const ShopModel: Model<Shop> = model('Shop', shopSchema);
