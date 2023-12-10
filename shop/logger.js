export const logger = (req, res, next) => {
    console.log(`Request: ${req.method} ${req.originalUrl}`);
    next();
    console.log(`Response: ${res.statusCode}`);
}
