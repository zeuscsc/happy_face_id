import {Request,Response} from 'express';
import fetch from 'node-fetch'
import { UserService } from '../services/UserService';

export class UserController{

    constructor(private userService:UserService){ }

    public login = async (req : Request, res : Response) => {
        // console.log("image",req.body)
        try {
            let results= await fetch("http://localhost:8000/get-identity",{
                method:"POST",
                body:req.body.image_base64
            })
            let identity=await results.json();
            // console.log(identity)
            if(identity.confidence<0.9){
                identity.classname="people"
            }
            let users=await this.userService.getUsersFromAi(identity.classname);
            let user=users[0];
            // console.log(users)
            res.json(user);
        } catch (error) {
            res.status(500).json({
                message: `Internal system error ${error.message}`,
            });
        }
    }
    public logout = (req : Request, res : Response) => {
        let username = req.session["username"];
        console.log(`${username} want to logout`);
        req.session.destroy((error) => {
            if (error) {
                console.error("failed to destroy session:", error);
            }
            
            res.redirect(`/index.html?user=${username}`);
        });
    }
    public get=async (req : Request, res : Response) => {
        if(req.session['user']){
            res.json({
                username: req.session['user'].username
            });
        }else{
            res.status(401).json({msg:"UnAuthorized"});
        }
    }
    public test=async (req : Request, res : Response) => {
        res.send("Working");
    }
}