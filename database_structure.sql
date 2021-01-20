CREATE TABLE Roles(
  id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);
CREATE TABLE Teams(
  id UUID PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);
CREATE TABLE Users(
  id UUID PRIMARY KEY NOT NULL,
  username TEXT NOT NULL,
  user_role INTEGER REFERENCES Roles NOT NULL,
  user_team UUID REFERENCES Teams,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT,
  profile_image TEXT
);
CREATE TABLE Permissions(
  task TEXT PRIMARY KEY NOT NULL,
  needed_role INTEGER REFERENCES Roles NOT NULL
);
CREATE TABLE Projects(
  id UUID PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT [],
  added_on TIMESTAMP NOT NULL
);
CREATE TABLE Features(
  id UUID PRIMARY KEY NOT NULL,
  project_id UUID REFERENCES Projects NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT [],
  status TEXT,
  priority INTEGER,
  added_on TIMESTAMP NOT NULL,
  ready TIMESTAMP
);
CREATE TABLE Tasks(
  id UUID PRIMARY KEY NOT NULL,
  feature_id UUID REFERENCES Features NOT NULL,
  assignee UUID REFERENCES Users NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  flags TEXT [],
  status TEXT,
  added_on TIMESTAMP NOT NULL,
  priority INTEGER,
  time_spent FLOAT,
  ready TIMESTAMP
);