"""This script is used to split the audio from the corpus of TikTok videos as
a pre-processing step for speech recognition.

Reference: https://towardsdatascience.com/extracting-speech-from-video-using-python-f0ec7e312d38"""
import moviepy.editor as mp
import json
import time


print("Loading JSON data...")
start = time.time()
with open("master.json","r",encoding="utf-8") as f:
    master_text = f.read()
tiktoks = json.loads(master_text)
print(f"Completed in {time.time()-start:.2f} seconds.\n")
#Load data from `master.json` to get ids of successful downloads.

print("Extracting audio from TikToks...")
start = time.time()
for (i,(id,tiktok)) in enumerate(tiktoks.items()):
    print(f"Extracting audio {i+1} / {len(tiktoks)}")
    if (tiktok["download-timestamp"] == None):
        print("File not downloaded.")
        #Tiktoks in `master.json` with a null download-timestamp were not
        #successfully downloaded (and neither were their cover photos).
        continue

    try:
        clip = mp.VideoFileClip(f"videos/{id}.mp4")
        #Load the video into MoviePy.
        clip.audio.write_audiofile(f"audios/{id}.wav")
        #Extract the audio.
    except Exception as e:
        print(e)
