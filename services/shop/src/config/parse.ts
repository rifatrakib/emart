import { AppConfig } from "../interfaces/config";

const config = require("../../config.json");

export const parseConfig = (): AppConfig => {
    return {
        app: process.env.APP_NAME || config.app,
        env: process.env.NODE_ENV || config.env,
        port: process.env.PORT || config.port,
        mongodbConfig: {
            username: process.env.MONGO_USERNAME || config.mongodbConfig.username,
            password: process.env.MONGO_PASSWORD || config.mongodbConfig.password,
            host: process.env.MONGO_HOST || config.mongodbConfig.host,
            port: process.env.MONGO_PORT || config.mongodbConfig.port,
        },
        corsOptions: config.corsOptions,
    };
};

export const appConfig: AppConfig = parseConfig();

const getDbUri = () => {
    const { mongodbConfig } = appConfig;
    const { username, password, host, port } = mongodbConfig;
    return username && password ? `mongodb://${username}:${password}@${host}:${port}` : `mongodb://${host}:${port}`;
};

export const mongoUri = getDbUri();
