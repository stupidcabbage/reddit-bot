create table if not exists subreddits(
  id integer primary key autoincrement,
  name text
);


create table if not exists flairs(
  name text primary key,
  subreddit_id integer,
  foreign key(subreddit_id) references subreddits(id)
);


create table if not exists posts(
  id integer primary key autoincrement,
  title text,
  description text,
  flair_name text null,
  subreddit_id integer not null,
  created_at timestamp default current_timestamp not null,
  foreign key(subreddit_id) references subreddits(id),
  unique(title, description)
);


create table if not exists medias(
  filename text,
  media_url text unique,
  file_type text,
  server_media_id integer,
  post_id integer,
  foreign key(post_id) references posts(id)
);
