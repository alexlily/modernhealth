create database modernhealth;
\c modernhealth;
create table if not exists programs ( id serial NOT NULL, name text, description text, CONSTRAINT programs_pkey PRIMARY KEY (id));
create table if not exists sections (id serial NOT NULL, program_id serial REFERENCES programs(id), name text, description text, orderindex integer, overview_image_id varchar, PRIMARY KEY (id));
create table if not exists activities (id serial NOT NULL, section_id serial REFERENCES sections(id), staticContent text, question_text text, answers text[], PRIMARY KEY (id) );

copy programs(name, description) FROM '/Users/alex/modernhealth/bootstrap/programs.csv' DELIMITER ',' CSV HEADER;
copy sections(program_id, name, description, orderindex, overview_image_id) FROM '/Users/alex/modernhealth/bootstrap/sections.csv' DELIMITER ',' CSV HEADER;
copy activities(section_id, staticContent, question_text, answers) FROM '/Users/alex/modernhealth/bootstrap/activities.csv' DELIMITER ',' CSV HEADER;
