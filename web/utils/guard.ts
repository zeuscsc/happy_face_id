import express from 'express'
export let adminGuard = (req: express.Request, res: express.Response, next: express.NextFunction) => {
    if (req.session?.['username']) {
        next();
    } else {
        res.status(401).end("This resources is only accessible by admin");
        // res.end('')
    }
};