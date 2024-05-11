export interface ResponseSchema {
    statusCode: number;
    success: boolean;
    body: any;
    message?: string;
}
