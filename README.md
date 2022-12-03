# TikTok-Retrieval
Information retrieval experiments on a small corpus of TikToks.

## Data Acquisition

This section details the processes by which the data were scraped, downloaded, processed, cleaned, and loaded into `data/tiktoks.db` for analysis.

### Scraping Information

The script `data/scraper.js` is used to extract information from TikTok's desktop site [tiktok.com](https://tiktok.com). To use this script, first ensure that you are viewing the layout in which the comments section is visible, as shown below. Clicking a video in the default layout will bring you to this layout.

<img src="misc/tiktok desktop.jpg" />

Next, paste the code from `data/scraper.js` into the console. Finally, initiate the scraping process by entering the following lines into the console.

```javascript
results = await scrape_tiktoks(100, delay=2000);
console.log(JSON.stringify(results));
```

The `scrape_tiktoks(n_to_scrape, delay)` function has two arguments; the `n_to_scrape` positional argument indicates the number of TikToks whose information will be scraped, while the `delay` keyword argument specifies a number of milliseconds to wait for a single TikTok's information to load before scraping it. In practice, I have found that using my home WiFi and using a premium VPN, 2000 ms tends to be sufficient for most videos; occasionally, the comments will take longer to load and will thus not be scraped, but 2000 ms strikes a good balance between speed and performance.

Once the call of `scrape_tiktoks` has concluded, the JSON-stringified results must be pasted into a json file in the `data/info/` folder.

The `scrape_tiktoks` function iteratively calls the `extract_tiktok_information` function, which obtains the following information for the focused TikTok:

- SRC of video tag (for downloading)
- SRC of cover photo img tag (for downloading)
- Permalink (for re-accessing)
- Web ID (I don't really know what this is; but I don't want to skip it
    in case it's important)
- ID
- Video like count
- Video comment count
- Uploader's username
- Uploader's nickname
- Title of music
- HREF of music a tag
- Video description text
- First ~20 top-level comments (including commenter name, comment text, like count, and time posted)
- Timestamp of info extraction

I copied code from [tutorialspoint.com/javascript-sleep-function](https://www.tutorialspoint.com/javascript-sleep-function) for the `delay` function, which blocks execution for a set duration.

#### To Do
- Use event listeners to ensure that comments have loaded before scraping instead of waiting a fixed amount of time.
    - Historically, I've had difficulty getting this to work, especially on enterprise websites, which is why I did it the way I did it.
- Scroll to the bottom of the comments section to collect all comments; expand replies to get nested comments.
    - I figured that this was more work than it was worth given the application of the data.
    - Also, I worried that having too many comments would dilute the actual content.
- Scraper does not have any way to handle Photo Mode TikToks (image slideshows); only videos.
    - Photo Mode is not available on the desktop website, so it worked out for now, but the scraper may break if Photo Mode comes to desktop.
- Scraper does not have a way to download auto-generated speech-to-text captions because closed captions are not available yet on the desktop app.


### Downloading Videos and Covers

Notably, JavaScript does not make it easy to automate downloading, so the Python script `data/downloader.py` is used to download the videos and coverphotos whose src links are included the JSON files containing raw scraped data. Beware: I looked at the values of the `expires` key for a few of these links, and it seems that they may only be valid for 8-12 hours, so don't wait to download the videos after you have scraped their info.

I copied the `download_file` function from [stackoverflow.com/questions/53196594/web-scraping-videos](https://stackoverflow.com/questions/53196594/web-scraping-videos), which uses the `requests` library to download a resource from a link.

The `download_tiktoks_from_info` function goes through the links in a batch of raw scraped information with error handling. Videos are saved to the `data/videos/` folder, coverphotos are saved to the `data/coverphotos/` folder, and info (including a new `download-timestamp` attribute) is saved as a dictionary of (id,info_dict) pairs to `data/master.json`.

I encountered several types of errors that can occur when trying to download a TikTok:
- `requests.exceptions.InvalidSchema: No connection adapters were found for '{video src}'`
    - This error occurs for TikToks whose video srcs are Blob URLs, which cannot be downloaded.
    - Sometimes, re-scraping the video's information will give a URL, but oftentimes Blob URLs are provided for videos on which downloading is disabled.
- `urllib3.util.ssl_match_hostname.CertificateError: hostname 'v19-webapp-prime.us.tiktok.com' doesn't match either of '*.hypstarcdn.com', 'hypstarcdn.com'`
    - This exception is succeeded by "During handling of the above exception, another exception occurred":
        - `HTTPSConnectionPool(host='v19-webapp-prime.us.tiktok.com', port=443): Max retries exceeded with url: ... (Caused by SSLError(CertificateError("hostname 'v19-webapp-prime.us.tiktok.com' doesn't match either of '*.hypstarcdn.com', 'hypstarcdn.com'")))`
    - More often than not, if we retry downloading the videos that raise this exception, it will go away.
    - If we get a lot of these in quick succession, it usually helps to connect to a different VPN server.  
- Very infrequently, there are links that will cause the downloader to hang indefinitely. I found that it was best to just skip them and move on.
    - Only two links yielded this problem: video 39 in batch 1 and video 184 in batch 2 (indexed starting with 1).

Videos that were successfully downloaded have a non-null `download-timestamp` attribute in `data/master.json` corresponding to the Unix timestamp after the download is complete, whereas videos that raised exceptions are logged with a null `download-timestamp`.

Running `data/download.py` a second time on a raw-info file will skip videos that were successfully downloaded the first time (as indicated by their non-null `download-timestamp` in `data/master.json`) and only re-try videos that were not successfully downloaded; if one of these downloads succeeds, the corresponding entry in `data/master.json` is overwritten.


### Optical Character Recognition

Following the tutorial at [builtin.com/data-science/python-ocr](https://builtin.com/data-science/python-ocr), the open source Tesseract OCR engine (v5.2.0.20220712) is used to extract text from cover photos. The script `data/ocr.py` uses the `pytesseract` library (v0.3.10), which provides a Python-based interface for Tesseract, to extract text from all of the cover photos whose TikTok ids are present in `data/master.json` and whose corresponding files (`{id}.jpg`) are present in `data/coverphotos`. Results are saved as a dictionary of (id,recognized_string) pairs to `data/ocr.json`.

Note: because `data/downloader.py` also logs information for TikToks that were unable to be downloaded, `data/ocr.py` skips any id for which there is not a corresponding file in `data/coverphotos`. Additionally, some photos are corrupted and raise a `PIL.UnidentifiedImageError` when attempting to load them. For these, we simply continue, assigning the ID to `NULL` (`None`) in `data/ocr.json`.

Performing OCR over the whole corpus of cover photos took ~45 minutes.


### Speech-to-Text

Following the tutorial at [towardsdatascience.com/extracting-speech-from-video-using-python-f0ec7e312d38](https://towardsdatascience.com/extracting-speech-from-video-using-python-f0ec7e312d38), the Python `SpeechRecognition` library (v3.8.1) is used to transcribe speech from the TikToks.

As a pre-processing step, the audio must be extracted from the videos as WAV files using the `MoviePy` library (v1.0.3), which took a total of around 30 minutes for the entire corpus. The Python script `data/extract_audio.py` extracts audio from the TikToks in `data/videos/` and saves the resulting WAV files to `data/audios/`. During this process, a very verbose error would occasionally occur. Upon deeper investigation, many of the videos that give this error are corrupted (probably a botched download). It is possible, too, that some videos are just missing audios because TikTok occasionally removes the sound from videos for copyright/censorship reasons.

The actual speech recognition occurs in the Python script `data/speech_to_text.py`, which runs speech recognition on the files in `data/audios` and saves the results to `data/speech_to_text.json`. The Python `SpeechRecognition` library provides an interface to several different recognition services; I use Google Speech, accessed through the `recognize_google` method of the `speech_recognition.Recognizer` class.

Google Speech returns a "Bad Request" error for audio files that are longer than ~2 minutes; I get around this by breaking up longer audio files into chunks whenever an error occurs.

Performing speech recognition on the entire corpus took around 3 hours.

### ETL

The Python script `data/json2db.py` is used to clean and combine the information in `data/master.json`, `data/ocr.json`, and `data/speech_to_text.json` and write them to `tiktoks.db`; a SQLite database that will serve as the data warehouse for the experiments.

The SQL file `data/initialize_tiktoks_db.sql` provides the data definition used to construct `data/tiktoks.db`. It creates two tables: `tiktoks`, which contains all of the information corresponding to a TikTok except for the comments, which are stored in the `comments` table, with their respective TikToks' ids as foreign keys. The BATCH file `initialize_tiktoks_db.bat` runs the following command to create the database file:

```batch
sqlite3 tiktoks.db < initialize_tiktoks_db.sql
```

Moving forward, we will only use TikToks for which the `download-timestamp`, as well as the coverphoto OCR and speech-to-text results are all non-null because a null `download-timestamp` indicates a missing download and a null coverphoto OCR or speech-to-text result usually indicates a corrupted/broken file.

The corpus of cleaned TikToks contains a total of 1462 TikToks. Their info is saved in `data/cleaned_master.json`, which is used in the viewing application.



## Generating Test Queries

TikTok retrieval is somewhat atypical in that often, when people are searching for a TikTok, they are looking for a single specific video that they have seen before and have since lost track of. In terms of retrieval, this means that it is more common than not for a query to only have a single relevant document. In this project, I am specifically focusing on these single-target queries.

In order to ensure that the test queries against which the retrieval systems are to be evaluated are realistic, I decided to solicit queries from friends. I tasked several friends to watch a handful of TikToks in my corpus, keep a few salient ones in mind, wait for a while to ensure that they've passed from short-term memory, and then come up with queries based on what they remember in order to find those TikToks again.


### Viewing Application

In order to streamline the process of soliciting queries, I constructed a web-based viewer application for my participants to use to watch videos in the corpus. The viewer application is located in `data/viewer/`; the main page is `data/viewer/index.php`.

The viewer itself is constructed such that it crudely resembles the TikTok desktop app in order to provide the participants a realistic viewing experience. Additionally, there is a "History" tab, which uses `window.localStorage` to track the view history of the participants and a "Search" tab, which performs ranked retrieval based on a rudimentary index. These features are to help the viewers find the IDs corresponding to the relevant TikToks of their queries because queries without relevance labels are no use to anyone.

### Instructions to Participants
Participants were given the following instructions.

    The goal of my experiment is to improve the process of searching for TikToks. In order to determine what works best, I need to quantify retrieval performance. The way to do this is to come up with a set of test queries with known targets and see if the system identifies the correct video for a given query.    

    I'm requesting your help to come up with queries in order to avoid injecting my own bias into the experiment. What I need you to do is:

    1. Go to jimtok.shepich.com and watch a handful of TikToks. It may take a while for the page to load.
    2. Do something else for an hour or so, in order to reset your short-term memory.
    3. Think of a few videos that stood out to you. For each one, come up with a query that you would use to search for it.
    4. Find the IDs corresponding to your query targets (either using the View History or Search tabs), and send me a list of (query text, query target id) pairs.

    Note: please come up with queries that are specific to an individual TikTok, rather than a trend or collection. My goal is to improve the ability to recall specific videos.

    Also note: the search feature does not work very well, so don't bank on that being very useful when you go back and look for IDs (hopefully I can change that with this project).

    WARNING: these TikToks have not been content-filtered, so participate at your own risk. Massive spoilers for Attack on Titan and One Piece ahead.

    Website controls:

     - Up/Left arrow: previous video in queue
     - Right/Down arrow: next video in queue
     - Space: play/pause video (first video will start paused)
     - Press "Enter" while typing in search bar to run your query (wait until page is loaded before searching)
     - Click on an ID in the View History or Search results to watch that video
     - Note: clicking on a link will not change the queue or your position in it, so you can click links without worrying about losing your place.

    Thank you for participating!

### Basic Index

UNIDECODE (converts greek letters and emojis into text)
ASCII
~20 seconds





experiment took about an hour to run on my single query


Unidecode 1.3.6
