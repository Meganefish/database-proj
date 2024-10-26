DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS moderators;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nickname VARCHAR(50)
);
CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    forum_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id),
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id)
);
CREATE TABLE forums (
    forum_id INTEGER PRIMARY KEY  AUTOINCREMENT,
    forum_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE moderators (
    moderator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    forum_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (forum_id) REFERENCES forums (forum_id)
);

INSERT INTO forums(forum_name, description)
VALUES ('学业', '有关学习'),
       ('选课','有关选课'),
       ('娱乐', '有关娱乐'),
       ('树洞', '有关树洞');