import express from 'express'
import expressSession from 'express-session'
import { print } from 'listening-on'
import { join, resolve } from 'path'
import http from 'http';
import grant from 'grant';
import env from './utils/env'
import { adminGuard } from './utils/guard'
import { UserService } from './services/UserService';
import { UserController } from './controllers/UserController';
import Knex from 'knex';
import dotenv from 'dotenv';
import {UserRoutes} from './routes/UserRoutes';

const knexConfigs = require('./knexfile');
const environment = process.env.NODE_ENV || 'development';
const knexConfig = knexConfigs[environment];
const knex = Knex(knexConfig);

dotenv.config();

const grantExpress = grant.express({
    "defaults":{
        "origin": "http://localhost:8080",
        "transport": "session",
        "state": true,
    },
    "google":{
        "key": env.GOOGLE_CLIENT_ID,
        "secret": env.GOOGLE_CLIENT_SECRET,
        "scope": ["profile","email"],
        "callback": "/login/google"
    }
});

const app = express()
const server = new http.Server(app);

// app.use(express.json())
// app.use(express.bodyParser({limit: '50mb'}));
app.use(express.json({ limit: "50mb" , strict: false }));

app.use(
  expressSession({
    secret: env.SESSION_SECRET ,
    resave: true,
    saveUninitialized: true,
  }),
)

app.use(grantExpress as express.RequestHandler);

declare module 'express-session' {
  interface SessionData {
    username?: string
  }
}

export const userService = new UserService(knex);
export const userController = new UserController(userService);

const userRoutes=UserRoutes(userController);
app.use(userRoutes);

app.use(express.static('public'))
app.use('/admin', adminGuard, express.static('admin'))

app.get("/",(req, res) => {
  res.sendFile(resolve(join("public","happy-face-id.html")))
})
app.use((req, res) => {
  res.sendFile(resolve(join('public', '404.html')))
})

let port = 8080
server.listen(port, () => {
  print(port)
})
