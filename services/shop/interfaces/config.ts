import { CorsOptions } from "cors";

export interface AppConfig {
    env: string;
    port: number;
    corsOptions: CorsOptions;
}
