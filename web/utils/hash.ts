import * as bcrypt from "bcryptjs";

const SALT_ROUNDS = 10;

export async function hashPassword(plainPassword: string): Promise<string> {
    const hash = await bcrypt.hash(plainPassword, SALT_ROUNDS);
    return hash;
}
export async function checkPassword(plainPassword: string, hashPassword: string): Promise<boolean> {
    const match = await bcrypt.compare(plainPassword, hashPassword);
    return match;
}

// async function hash(){
//     let inputPassword = "admin"
//     let hasedPassword = await hashPassword(inputPassword)

//     console.log(`1 ${inputPassword}  ----> ${hasedPassword}`)
//     let isValid = await checkPassword("admin",hasedPassword )
//     console.log('password checked:', isValid)
// }

// hash()
