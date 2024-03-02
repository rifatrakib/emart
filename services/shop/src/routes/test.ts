import { Body, Controller, Post, Route } from 'tsoa';
import { Test } from '../controllers/schemas/test';
import { TestCreateParams, TestService } from '../controllers/services/test';

@Route('test')
export class TestController extends Controller {
    @Post()
    public async createTest(
        @Body() body: TestCreateParams
    ): Promise<Test> {
        return await new TestService().create(body);
    }
}
