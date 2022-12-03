CREATE TABLE tiktoks(
    id INT NOT NULL,
    web_id INT NOT NULL,
    permalink TEXT NOT NULL,
    video_src TEXT NOT NULL,
    coverphoto_src TEXT NOT NULL,
    music_src TEXT NOT NULL,
    speech_to_text TEXT,
    coverphoto_ocr TEXT,
    music_title TEXT NOT NULL,
    like_count TEXT NOT NULL,
    comment_count TEXT NOT NULL,
    creator_username TEXT NOT NULL,
    creator_nickname TEXT,
    description TEXT,
    time_posted TEXT NOT NULL,
    scrape_timestamp FLOAT NOT NULL,
    download_timestamp FLOAT,
    PRIMARY KEY (id)
);

CREATE TABLE comments(
    video_id INT NOT NULL,
    like_count TEXT NOT NULL,
    replies_count TEXT,
    comment_text TEXT NOT NULL,
    commenter_name TEXT NOT NULL,
    time_posted TEXT NOT NULL,
    FOREIGN KEY (video_id) REFERENCES tiktoks(id)
);
