# TikTok-Retrieval
Information retrieval experiments on a small corpus of TikToks.

# Data Acquisition

This section details the processes by which the data were scraped, downloaded, processed, cleaned, and loaded into `data/tiktoks.db` for analysis.

## Scraping Information

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

### To Do
- Use event listeners to ensure that comments have loaded before scraping instead of waiting a fixed amount of time.
    - Historically, I've had difficulty getting this to work, especially on enterprise websites, which is why I did it the way I did it.
- Scroll to the bottom of the comments section to collect all comments; expand replies to get nested comments.
    - I figured that this was more work than it was worth given the application of the data.
    - Also, I worried that having too many comments would dilute the actual content.
- Scraper does not have any way to handle Photo Mode TikToks (image slideshows); only videos.
    - Photo Mode is not available on the desktop website, so it worked out for now, but the scraper may break if Photo Mode comes to desktop.
- Scraper does not have a way to download auto-generated speech-to-text captions because closed captions are not available yet on the desktop app.


## Downloading Videos and Covers

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


## Optical Character Recognition

The open source Tesseract OCR engine (v5.2.0.20220712) is used to extract text from cover photos. The script `data/ocr.py` uses the `pytesseract` library (v0.3.10), which provides a Python-based interface for Tesseract, to extract text from all of the cover photos whose TikTok ids are present in `data/master.json` and whose corresponding files (`{id}.jpg`) are present in `data/coverphotos`. Results are saved as a dictionary of (id,recognized_string) pairs to `data/ocr.json`.

Note: because `data/downloader.py` also logs information for TikToks that were unable to be downloaded, `data/ocr.py` skips any id for which there is not a corresponding file in `data/coverphotos`. Additionally, some photos are corrupted and raise a `PIL.UnidentifiedImageError` when attempting to load them. For these, we simply continue, assigning the ID to `NULL` (`None`) in `data/ocr.json`.

Performing OCR over the whole corpus of cover photos took about a half hour.


## Speech-to-Text



##
