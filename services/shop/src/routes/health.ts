import { Controller, Get, Route } from 'tsoa';
import { HealthCheck } from '../controllers/schemas/health';
import { HealthService } from '../controllers/services/health';

@Route('health')
export class HealthController extends Controller {
    @Get("")
    public async healthCheck(): Promise<HealthCheck> {
        return new HealthService().get();
    }
}
