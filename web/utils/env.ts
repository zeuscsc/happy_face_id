import dotenv from "dotenv";
dotenv.config();


const env = {
    DB_NAME: process.env.DB_NAME || "memo_wall",
    DB_USERNAME: process.env.DB_USERNAME || "postgres",
    DB_PASSWORD: process.env.DB_PASSWORD || "postgres",
    GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET,
    SESSION_SECRET: process.env.SESSION_SECRET || "DEFAULT SESSION SECRET"
};

export default env;