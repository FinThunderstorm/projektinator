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
  username TEXT NOT NULL CHECK(LENGTH(username) >= 5),
  user_role SERIAL REFERENCES Roles NOT NULL,
  password_hash TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT CHECK(email LIKE '%@%.%'),
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
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Features(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  project_id uuid REFERENCES Projects NOT NULL,
  feature_owner uuid REFERENCES Users NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT,
  status TEXT,
  type TEXT,
  priority INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
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
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Comments(
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  feature_id uuid REFERENCES Features,
  task_id uuid REFERENCES Tasks,
  comment TEXT NOT NULL,
  assignee uuid REFERENCES Users,
  added_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Teamsusers(
  user_id uuid NOT NULL PRIMARY KEY REFERENCES Users,
  team_id uuid NOT NULL REFERENCES Teams
);
CREATE OR REPLACE FUNCTION updated_on() RETURNS trigger AS $$ BEGIN NEW.updated_on = now();
RETURN NEW;
END;
$$ language 'plpgsql';
CREATE TRIGGER updated_on BEFORE
UPDATE ON Projects FOR EACH ROW EXECUTE PROCEDURE updated_on();
CREATE TRIGGER updated_on BEFORE
UPDATE ON Features FOR EACH ROW EXECUTE PROCEDURE updated_on();
CREATE TRIGGER updated_on BEFORE
UPDATE ON Tasks FOR EACH ROW EXECUTE PROCEDURE updated_on();
CREATE TRIGGER updated_on BEFORE
UPDATE ON Comments FOR EACH ROW EXECUTE PROCEDURE updated_on();