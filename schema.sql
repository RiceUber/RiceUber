DROP TABLE IF EXISTS [entries];
CREATE TABLE entries (
  id integer primary key autoincrement,
  name text not null,
  email text not null,
  phone text not null,
  datetime text not null,
  fromloc text not null,
  toloc text not null
);