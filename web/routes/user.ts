import express from "express";
// import { red, reset } from "asciichart";
import { client } from "../utils/db";
import { checkPassword, hashPassword } from "../utils/hash";
import fetch from 'node-fetch'
import { v4 as uuidv4 } from 'uuid';
import { User } from "../models/user";

export let userRoutes = express.Router();

userRoutes.use(express.urlencoded({ extended: false }));

let login = async (req : express.Request, res : express.Response) => {
    try {
        let results= await fetch("localhost:8000/get-identity")
    } catch (error) {
        res.status(500).json({
            message: "Internal system error",
        });
    }
}

let getMe = (req : express.Request, res : express.Response) => {
    let currentUser = req.session["username"] ? req.session["username"] : "NA";
    res.json({
        user: currentUser,
    });
}
let logout = (req : express.Request, res : express.Response) => {
    let username = req.session["username"];
    console.log(`${username} want to logout`);
    req.session.destroy((error) => {
        if (error) {
            console.error("failed to destroy session:", error);
        }
        
        res.redirect(`/index.html?user=${username}`);
    });
}


userRoutes.post("/login",login);
userRoutes.get("/me", getMe);
userRoutes.post("/logout", logout);