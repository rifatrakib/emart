export const logger = (req, res, next) => {
    next();
    console.log(`${req.method} ${req.url} ${res.statusCode}`);
}
