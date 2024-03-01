import { HealthCheck } from "../schemas/health";
import config from "../../config/env";

export class HealthService {
    public get(): HealthCheck {
        return {
            port: config.PORT,
        };
    }
}
