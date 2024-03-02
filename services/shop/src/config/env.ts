import dotenv from 'dotenv';

dotenv.config();

interface AppConfig {
    PORT: number;
    DATABASE_URI: string;
}

const settings: AppConfig = ((): AppConfig => {
    const settings: AppConfig = {
        PORT: parseInt(process.env.PORT || "3000", 10),
        DATABASE_URI: process.env.DATABASE_URL || "",
    }
    if (!settings.DATABASE_URI) {
        throw new Error("DATABASE_URL is not set");
    }
    return settings
})();

export default settings;
