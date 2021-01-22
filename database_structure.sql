CREATE TABLE Roles(
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);
CREATE TABLE Teams(
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);
CREATE TABLE Users(
  id SERIAL PRIMARY KEY NOT NULL,
  username TEXT NOT NULL,
  user_role SERIAL REFERENCES Roles NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT,
  profile_image TEXT
);
CREATE TABLE Permissions(
  task TEXT PRIMARY KEY NOT NULL,
  needed_role SERIAL REFERENCES Roles NOT NULL
);
CREATE TABLE Projects(
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT [],
  added_on TIMESTAMP NOT NULL
);
CREATE TABLE Features(
  id SERIAL PRIMARY KEY NOT NULL,
  project_id SERIAL REFERENCES Projects NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT [],
  status TEXT,
  priority INTEGER,
  added_on TIMESTAMP NOT NULL,
  ready TIMESTAMP
);
CREATE TABLE Tasks(
  id SERIAL PRIMARY KEY NOT NULL,
  feature_id SERIAL REFERENCES Features NOT NULL,
  assignee SERIAL REFERENCES Users NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT [],
  status TEXT,
  added_on TIMESTAMP NOT NULL,
  priority INTEGER,
  time_spent FLOAT,
  ready TIMESTAMP
);
CREATE TABLE Comments(
  id SERIAL PRIMARY KEY NOT NULL,
  feature_id SERIAL REFERENCES Features,
  task_id SERIAL REFERENCES Tasks,
  comment TEXT NOT NULL,
  assignee SERIAL REFERENCES Users,
  added_on TIMESTAMP NOT NULL
);
CREATE TABLE Teamsusers(
  user_id SERIAL NOT NULL,
  team_id SERIAL NOT NULL
);