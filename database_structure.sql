CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE Roles(
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);
CREATE TABLE Teams(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  name TEXT NOT NULL,
  description TEXT
);
CREATE TABLE Users(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  username TEXT NOT NULL,
  user_role SERIAL REFERENCES Roles NOT NULL,
  password_hash TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT,
  profile_image TEXT,
  UNIQUE(username)
);
CREATE TABLE Permissions(
  task TEXT PRIMARY KEY NOT NULL,
  needed_role SERIAL REFERENCES Roles NOT NULL
);
CREATE TABLE Projects(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  project_owner uuid REFERENCES Users NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT,
  created TIMESTAMP NOT NULL
);
CREATE TABLE Features(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  project_id uuid REFERENCES Projects NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT,
  status TEXT,
  type TEXT,
  priority INTEGER,
  created TIMESTAMP NOT NULL,
  updated_on TIMESTAMP
);
CREATE TABLE Tasks(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  feature_id uuid REFERENCES Features NOT NULL,
  assignee uuid REFERENCES Users NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT,
  status TEXT,
  type TEXT,
  priority INTEGER,
  created TIMESTAMP NOT NULL,
  updated_on TIMESTAMP
);
CREATE TABLE Comments(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  feature_id uuid REFERENCES Features,
  task_id uuid REFERENCES Tasks,
  comment TEXT NOT NULL,
  assignee uuid REFERENCES Users,
  added_on TIMESTAMP NOT NULL
);
CREATE TABLE Teamsusers(
  user_id uuid NOT NULL,
  team_id uuid NOT NULL
);