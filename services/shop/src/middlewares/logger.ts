import { Request, Response, NextFunction } from 'express';

export const logger = async (req: Request, res: Response, next: NextFunction) => {
    next();
    const remote = `${req.hostname}:${req.socket.remotePort}`;
    const timestamp = new Date().toLocaleString();
    const method = req.method.padEnd(5);
    const url = req.originalUrl;
    const status = res.statusCode.toString().padEnd(5);

    console.log(`[${timestamp}] ${remote} ..... ${status} ${method} ${url}`);
}
