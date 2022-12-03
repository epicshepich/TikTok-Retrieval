"""This script uses the SpeechRecognition library to recognize speech text
from the audio files in  `data/audios/` directory.

Reference: https://towardsdatascience.com/extracting-speech-from-video-using-python-f0ec7e312d38"""
import speech_recognition as sr
import json
import time
import os

print("Loading JSON data...")
start = time.time()
with open("master.json","r",encoding="utf-8") as f:
    master_text = f.read()
tiktoks = json.loads(master_text)
#Load data from `master.json` to get ids of successful downloads.

sr_results = {}
try:
    with open("speech_to_text.json","r",encoding="utf-8") as f:
        sr_results_text = f.read()
    sr_results = json.loads(sr_results_text)
except FileNotFoundError:
    pass
#Load saved speech recognition results to avoid re-processing.

print(f"Completed in {time.time()-start:.2f} seconds.\n")



def recognize_long(audio: sr.AudioFile, chunk_size=60, offset=0):
    """This function handles audio files that are larger than Google's limit
    by breaking them up into chunks of a fixed, smaller duration and
    recursively listening to successive chunks until one is empty."""
    result = ""
    recognizer = sr.Recognizer()
    try:
        with audio as source:
            audio_file = recognizer.record(source,offset=offset,duration=chunk_size)
        result = recognizer.recognize_google(audio_file)
    except sr.UnknownValueError:
        result = ""

    if result != "":
        result += " " + recognize_long(audio, chunk_size=chunk_size, offset=offset+chunk_size)
        #If the result is nonempty, then increment the offset by the chunk size
        #and call the function on the next chunk, piecing the results together.

    return result


print("Performing speech recognition on audio files...")
start = time.time()
for (i,(id,tiktok)) in enumerate(tiktoks.items()):
    if id in sr_results:
        continue
        #Skip TikToks that have already been successfully processed.
    print(f"Recognizing speech {i+1} / {len(tiktoks)}")
    if (tiktok["download-timestamp"] == None):
        print("File not downloaded.")
        #Tiktoks in `master.json` with a null download-timestamp were not
        #successfully downloaded (and neither were their cover photos).
        continue

    if not (os.path.isfile(f"audios/{id}.wav")):
        sr_results[id] = None
        continue
        #If the audio file is missing from the directory, log a null value for
        #the id.
    try:
        recognizer = sr.Recognizer()
        audio = sr.AudioFile(f"audios/{id}.wav")
        with audio as source:
            audio_file = recognizer.record(source)
        sr_results[id] = recognizer.recognize_google(audio_file)
        #Use the Google speech recognition API to generate the result.
    except sr.UnknownValueError:
        print(f"No speech recognized: {id}")
        sr_results[id] = ""
        #If the recognizer fails to identify any speech, log an empty string
        #(we only want to filter out truly erroneous data).
    except sr.RequestError:
        print(f"Audio too long: {id}\nTrying smaller chunks.")
        audio = sr.AudioFile(f"audios/{id}.wav")
        sr_results[id] = recognize_long(audio)
        #A speech_recognition.RequestError is raised when the file is above
        #the limit set by Google, so we have to break the file up into chunks.


    if (i+1) % 5 == 0:
        with open("speech_to_text.json","w",encoding="utf-8") as f:
            json.dump(sr_results, f, indent=4)
            #Save results every 5 iterations in case of errors.


print(f"Completed in {time.time()-start:.2f} seconds.\n")


print("Saving results...")
start = time.time()
with open("speech_to_text.json","w",encoding="utf-8") as f:
    json.dump(sr_results, f, indent=4)
print(f"Completed in {time.time()-start:.2f} seconds.\n")
#Save the results to `data/speech_to_text.json`.
