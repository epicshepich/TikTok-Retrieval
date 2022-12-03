import json
import sqlite3
import time


print("Loading JSON data...")
start = time.time()
with open("master.json","r",encoding="utf-8") as f:
    master_text = f.read()
tiktoks = json.loads(master_text)
cleaned_tiktoks = {}
#Keep track of which TikToks didn't have any errors.
with open("ocr.json","r",encoding="utf-8") as f:
    ocr_text = f.read()
ocr_results = json.loads(ocr_text)
with open("speech_to_text.json","r",encoding="utf-8") as f:
    sr_text = f.read()
sr_results = json.loads(sr_text)
print(f"Completed in {time.time()-start:.2f} seconds.\n")

print("Reading existing results from database...")
start = time.time()
con = sqlite3.connect("tiktoks.db")
cur = con.cursor()
cur.execute("""SELECT id FROM tiktoks;""")
ids_in_database = set(cur.fetchall())
con.close()
print(f"Completed in {time.time()-start:.2f} seconds.\n")


print("Writing results to database...")
start = time.time()
con = sqlite3.connect("tiktoks.db")
cur = con.cursor()
for (i,(id,tiktok)) in enumerate(tiktoks.items()):
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
        sr_results.get(id,None),
        ocr_results.get(id,None),
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

    if (tiktok["download-timestamp"] is not None) and (sr_results.get(id,None) is not None) and (ocr_results.get(id,None) is not None):
        cleaned_tiktoks[id] = tiktok
        cleaned_tiktoks[id]["speech-to-text"] = sr_results[id]
        cleaned_tiktoks[id]["coverphoto-ocr"] = ocr_results[id]
        #Track which TikToks are error-free.

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
            comment["commenter-username"],
            comment["time-posted"]
        )
        )


con.commit()
con.close()
print(f"Completed in {time.time()-start:.2f} seconds.\n")

with open("cleaned_master.json","w",encoding="utf-8") as f:
    json.dump(cleaned_tiktoks, f, indent=4)
