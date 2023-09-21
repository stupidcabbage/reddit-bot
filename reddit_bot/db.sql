create table if not exists subreddits(
  id integer primary key autoincrement,
  name text
);


create table if not exists flairs(
  id integer primary key autoincrement,
  name text,
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
  is_published boolean default false not null,
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

insert into subreddits(name) values
("FortniteLeaks"),
("FortniteMemes"),
("FortNiteBR");


/* FortniteLeaks */
insert into flairs(subreddit_id, name) values
(1, "all");

/* FortniteMemes */
insert into flairs(subreddit_id, name) values
(2, "all");

/* FortNiteBR */
insert into flairs(subreddit_id, name) values
(3, "EPIC"),
(3, "EPIC REPLY"),
(3, "MOD"),
(3, "MEDIA"),
(3, "CLIP 🎬"),
(3, "STREAMER"),
(3, "HUMOR"),
(3, "TUTORIAL");
