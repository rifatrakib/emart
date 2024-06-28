import { CorsOptions } from 'cors';

interface DbConfig {
    host: string;
    port: number;
    username: string;
    password: string;
}

export interface AppConfig {
    app: string;
    env: string;
    port: number;
    pageSize: number;
    mongodbConfig: DbConfig;
    corsOptions: CorsOptions;
}
