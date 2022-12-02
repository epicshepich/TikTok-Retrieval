import json
import sqlite3
import time


print("Loading JSON data...")
start = time.time()
with open("master.json","r",encoding="utf-8") as f:
    master_text = f.read()
tiktoks = json.loads(master_text)
print(f"Completed in {time.time()-start:.2f} seconds.\n")

print("Reading existing results from database...")
start = time.time()
con = sqlite3.connect("tiktoks.db")
cur = con.cursor()
cur.execute("""SELECT id FROM tiktoks;""")
ids_in_database = set(cur.fetchall())
con.close()
print(f"Completed in {time.time()-start:.2f} seconds.\n")

print("Performing OCR on cover photos...")
start = time.time()
for (i,tiktok) in enumerate(tiktoks):
    if tiktok["id"] in ids_in_database:
        continue

    print(f"Extracting text {i+1} / {len(tiktoks)}")

    tiktok["speech-to-text"] = ""
    tiktok["coverphoto-ocr"] = ""


print(f"Completed in {time.time()-start:.2f} seconds.\n")


print("Writing results to database...")
start = time.time()
con = sqlite3.connect("tiktoks.db")
cur = con.cursor()
for (i,tiktok) in enumerate(tiktoks):
    print(f"Writing result {i+1} / {len(tiktoks)}")
    cur.execute(
    """INSERT INTO tiktoks(
        id,
        web_id,
        permalink,
        video_src,
        coverphoto_src,
        music_src,
        speech_to_text,
        coverphoto_ocr,
        music_title,
        like_count,
        comment_count,
        creator_username,
        creator_nickname,
        description,
        time_posted,
        scrape_timestamp,
        download_timestamp
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",
    (
        tiktok["id"],
        tiktok["web-id"],
        tiktok["permalink"],
        tiktok["video-src"],
        tiktok["coverphoto-src"],
        tiktok["music-src"],
        tiktok["speech-to-text"],
        tiktok["coverphoto-ocr"],
        tiktok["music-title"],
        tiktok["like-count"],
        tiktok["comment-count"],
        tiktok["creator-username"],
        tiktok["creator-nickname"],
        tiktok["description"],
        tiktok["time-posted"],
        tiktok["scrape-timestamp"],
        tiktok["download-timestamp"]
    )
    )

    for comment in tiktok["comments"]:
        cur.execute("""INSERT INTO comments(
            video_id,
            like_count,
            replies_count,
            comment_text,
            commenter_name,
            time_posted
        ) VALUES (?,?,?,?,?,?);""",
        (
            tiktok["id"],
            comment["like-count"],
            comment["replies-count"],
            comment["comment-text"],
            comment["commenter-name"],
            comment["time-posted"]
        )
        )


con.commit()
con.close()
print(f"Completed in {time.time()-start:.2f} seconds.\n")
