import { Knex } from "knex";


export async function up(knex: Knex): Promise<void> {
    await knex.schema.createTable('users',table=>{
        table.increments();
        table.string('username');
        table.string('ai_classname');
        table.string('job_title');
        table.string('articles_count');
        table.string('followers_count');
        table.string('following_count');
        table.timestamps(false,true);
    })
}


export async function down(knex: Knex): Promise<void> {
    await knex.schema.dropTableIfExists('users');
}

