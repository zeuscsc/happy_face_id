import { Knex } from "knex";
export class UserService{
    constructor(private knex:Knex){}
    
    async getUsers(username:string){
        return this.knex.select('*').from('users').where('username',username);
    }
    async getUsersFromAi(ai_classname:string){
        return this.knex.select('*').from('users').where('ai_classname',ai_classname);
    }
}