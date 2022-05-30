import express from "express";
import { UserController } from "../controllers/UserController";
// import {userController} from "../Server"


export function UserRoutes(userController:UserController){
    const userRoutes = express.Router();
    userRoutes.use(express.urlencoded({ extended: false }));
    userRoutes.post('/login',userController.login);
    userRoutes.post('/logout',userController.logout);
    userRoutes.post('/test',userController.test);
    userRoutes.get('/user/get/current',userController.get);
    return userRoutes;
}