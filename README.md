# SQL CRUD

The following is SQL CRUD operations solving problems introduced in the [instructions](/instructions.md)

## PART 1 - RESTURANT FINDER

Find the data in (.csv format) for the first part [here](data/resturants.csv).

## importing data

```SQL

.open resturant_db.db
.mode csv
.headers on


DROP TABLE IF EXISTS resturants;
CREATE table resturants(
  id INTEGER PRIMARY KEY,
  resturant_name TEXT,
  neighborhood TEXT,
  category TEXT,
  price_tier TEXT,
  resturant_open TIME,
  resturant_close TIME,
  average_rating FLOAT,
  good_for_kids INTEGER
);

.import data/resturants.csv resturants --skip 1;

DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    review_col TEXT
);

INSERT INTO reviews (id) SELECT id FROM resturants;

UPDATE resturants SET resturant_open =   '0' || resturant_open;


```

#### 1) Find all cheap restaurants in a particular neighborhood (pick any neighborhood as an example).

```SQL

SELECT resturant_name from resturants where neighborhood = "Bushwick" and price_tier = "Cheap";


```

#### 2)Find all restaurants in a particular genre (pick any genre as an example) with 3 stars or more, ordered by the number of stars in descending order.


```SQL

SELECT resturant_name,average_rating from resturants where category = "Mexican" and average_rating >= 3 order by average_rating DESC;

```

#### 3) Find all restaurants that are open now (see hint below).

```SQL

SELECT resturant_name from resturants where strftime ('%H:%M', 'now', 'localtime') BETWEEN strftime('%H:%M', resturant_open) AND strftime('%H:%M', resturant_close);

```

#### 4) Leave a review for a restaurant (pick any restaurant as an example).

```SQL

UPDATE reviews SET review_col = IFNULL(review_col || '; ', '') || 'Loved the food!' || '; ' WHERE id = 10;


```

#### 5) Delete all restaurants that are not good for kids.

```SQL

delete from resturants where good_for_kids = 0;


```

#### 6) Find the number of restaurants in each NYC neighborhood.


```SQL

select neighborhood, count(id) from resturants group by neighborhood;


```

## PART 2 - SOCIAL MEDIA APP

 - Find the data (in .csv format) for the posts [here](data/posts.csv).
 - Find the data (in .csv format) for the users [here](data/users.csv).



## importing data

```SQL
.open sm.db
.mode csv
.headers on

DROP TABLE IF EXISTS users;
CREATE table users(
  id INTEGER PRIMARY KEY,
  handle TEXT,
  email TEXT,
  password TEXT
);

.import data/users.csv users --skip 1;


DROP TABLE IF EXISTS posts;
CREATE table posts(
  id INTEGER PRIMARY KEY,
  id_sent INTEGER,
  message TEXT,
  viewed INTEGER,
  id_recieved INTEGER,
  stories TEXT,
  event_datetime TIME
);

.import data/posts.csv posts --skip 1;


```

#### 1) Register a new User.

```SQL

insert into users(
  handle,
  email,
  password
)

values("DataWizard","datawiz@snailmail.net", "Pikachu");


```

#### 2) Create a new Message sent by a particular User to a particular User (pick any two Users for example).

```SQL

insert into posts(
  id_sent,
  message,
  id_recieved,
  event_datetime
)

values(1,"Hey, this is a super secret message", 10, strftime('%Y-%m-%d %H:%M:%S', 'now'));


```

#### 3) Create a new Story by a particular User (pick any User for example).

```SQL
insert into posts(
  id_sent,
  stories,
  event_datetime
)

values(524, "My first story post!", strftime('%Y-%m-%d %H:%M:%S', 'now'));

```

#### 4) Show the 10 most recent visible Messages and Stories, in order of recency.

```SQL

select event_datetime, message, stories from posts order by event_datetime desc limit 10;

```

#### 5) Show the 10 most recent visible Messages sent by a particular User to a particular User (pick any two Users for example), in order of recency.

```SQL

SELECT event_datetime, message FROM posts WHERE viewed = 1 AND id_sent = 865 AND id_recieved = 627 ORDER BY event_datetime DESC LIMIT 10;

```

#### 6) Make all Stories that are more than 24 hours old invisible.


```SQL

UPDATE posts set viewed = 1 WHERE message IS "" and
(ROUND((JULIANDAY('now') - JULIANDAY(event_datetime)) * 24)) > 24;

 

```

#### 7) Show all invisible Messages and Stories, in order of recency.

```SQL

select message, stories, event_datetime FROM posts WHERE viewed = 1 ORDER BY JULIANDAY(event_datetime) DESC;

```

#### 8) Show the number of posts by each User.

```SQL

SELECT users.id, COUNT(posts.id)
FROM posts
JOIN users ON posts.id_sent = users.id
GROUP BY users.id;


```


#### 9) Show the post text and email address of all posts and the User who made them within the last 24 hours.

```SQL

SELECT message, stories, users.email, event_datetime
FROM posts 
JOIN users ON posts.id_sent = users.id 
WHERE ((ROUND((JULIANDAY('now') - JULIANDAY(event_datetime)) * 24)) < 24) LIMIT 15;

```

#### 10) Show the email addresses of all Users who have not posted anything yet.
```SQL

SELECT users.email FROM users LEFT JOIN posts ON  users.id = posts.id_sent WHERE posts.id_sent IS NULL;

```
