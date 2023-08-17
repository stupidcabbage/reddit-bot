create table if not exists subreddits(
  id integer primary key,
  name text
);


create table if not exists flairs(
  id integer primary key,
  name text,
  subreddit_id integer,
  foreign key(subreddit_id) references subreddits(id)
);


create table if not exists posts(
  id integet primary key,
  title text,
  description text,
  flair_id integer null,
  created_at timestamp default current_timestamp not null,
  foreign key(flair_id) references flairs(id)
);


create table if not exists medias(
  id integer primary key,
  filename text,
  media_url text,
  file_type text,
  post_id integer,
  foreign key(post_id) references posts(id)
);
