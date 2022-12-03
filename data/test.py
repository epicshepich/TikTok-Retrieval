#https://towardsdatascience.com/extracting-speech-from-video-using-python-f0ec7e312d38

import speech_recognition as sr


#7165609653135478058.wav

recognizer = sr.Recognizer()
audio = sr.AudioFile("audios/7071396378085231914.wav")
#7169259281970138414 - error big straw hat cm
#7086195168939986218 - gnome
#7071396378085231914 - lgbt professor


def record_long(audio: sr.AudioFile, chunk_size=60, offset=0):
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
        result += " " + record_long(audio, chunk_size=chunk_size, offset=offset+chunk_size)
        #If the result is nonempty, then increment the offset by the chunk size
        #and call the function on the next chunk, piecing the results together.

    return result

try:
    print(record_long(audio,400))
except sr.RequestError:
    print("poop")
