import { getDbConnection } from '../config/db';
import { mongoUri } from '../config/parse';

export const initDb = async () => {
    try {
        getDbConnection(mongoUri);
        console.log('MongoDB database connection established successfully.');
    } catch (error) {
        console.error(`Error connecting to MongoDB: ${error}`);
    }
};
