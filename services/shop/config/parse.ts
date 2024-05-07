import { AppConfig } from "../interfaces/config";

const config = require("../../config.json");

export const parseConfig = (): AppConfig => {
    return {
        env: process.env.NODE_ENV || config.env,
        port: process.env.PORT || config.port,
        corsOptions: config.corsOptions
    };
};
