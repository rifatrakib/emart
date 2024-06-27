import mongoose, { Error } from 'mongoose';

import { mongoUri } from './parse';

mongoose.set('strictQuery', true);

export const connectDb = async () => {
    const conn = mongoose.createConnection(mongoUri);

    conn.on('connected', () => console.log('Connected to MongoDB'));
    conn.on('open', () => console.log('MongoDB connection opened'));
    conn.on('disconnected', () => console.log('Disconnected from MongoDB'));
    conn.on('reconnected', () => console.log('Reconnected to MongoDB'));
    conn.on('disconnecting', () => console.log('Disconnecting from MongoDB'));
    conn.on('close', () => console.log('MongoDB connection closed'));
    conn.on('error', (err: Error) => console.error('MongoDB error:', err));

    return conn;
};
