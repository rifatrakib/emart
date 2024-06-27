import { connectDb } from '../config/db';

export const initDb = async () => {
    try {
        await connectDb();
        console.log('MongoDB database connection established successfully.');
    } catch (error) {
        console.error(`Error connecting to MongoDB: ${error}`);
    }
};
