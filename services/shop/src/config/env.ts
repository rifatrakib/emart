import dotenv from 'dotenv';

dotenv.config();

interface AppConfig {
    PORT: number;
}

const settings: AppConfig = {
    PORT: parseInt(process.env.PORT || "3000", 10),
}

export default settings;
