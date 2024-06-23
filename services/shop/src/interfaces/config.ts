import { CorsOptions } from "cors";

export interface AppConfig {
    app: string;
    env: string;
    port: number;
    corsOptions: CorsOptions;
}
