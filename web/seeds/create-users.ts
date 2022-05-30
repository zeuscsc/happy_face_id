import { Knex } from "knex";

export async function seed(knex: Knex): Promise<void> {
    // Deletes ALL existing entries
    await knex("users").del();

    // Inserts seed entries
    await knex("users").insert([
        { username: "Unknown" ,ai_classname:"people",job_title:"Unknown",articles_count:"NA",followers_count:"NA",following_count:"NA"},
        { username: "Zeus" ,ai_classname:"zeus",job_title:"Inventor",articles_count:"9000+",followers_count:"0",following_count:"200+"},
        { username: "Winnie" ,ai_classname:"winnie",job_title:"God of the Universe",articles_count:"NAN,",followers_count:"140,000,000",following_count:"1"},
    ]);
};
