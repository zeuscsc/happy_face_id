import env from './env'
import pg from "pg";

export const client = new pg.Client({
    database: env.DB_NAME,
    user: env.DB_USERNAME,
    password: env.DB_PASSWORD,
  });
  

  export function connectDB(){
    client.connect()
  }
  