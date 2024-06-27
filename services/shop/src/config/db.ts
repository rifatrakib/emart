import mongoose, { Error } from 'mongoose';

mongoose.set('strictQuery', true);

export const getDbConnection = (uri: string) => {
    const conn = mongoose.createConnection(uri);

    conn.on('connected', () => console.log('Connected to MongoDB'));
    conn.on('open', () => console.log('MongoDB connection opened'));
    conn.on('disconnected', () => console.log('Disconnected from MongoDB'));
    conn.on('reconnected', () => console.log('Reconnected to MongoDB'));
    conn.on('disconnecting', () => console.log('Disconnecting from MongoDB'));
    conn.on('close', () => console.log('MongoDB connection closed'));
    conn.on('error', (err: Error) => console.error('MongoDB error:', err));

    return conn;
};
