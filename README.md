# TikTok-Retrieval
 Information retrieval experiments on a small corpus of TikToks

# Data Collection

## Scraping Information

The script `data/scraper.js` is used to extract information from TikTok's desktop site [tiktok.com](https://tiktok.com). To use this script, first ensure that you are viewing the layout in which the comments section is visible, as shown below. Clicking a video in the default layout will bring you to this layout.

<img src="misc/tiktok desktop.jpg" />

Next, paste the code from `data/scraper.js` into the console. Finally, initiate the scraping process by entering the following lines into the console.

```javascript
results = await scrape_tiktoks(100, delay=2000);
console.log(JSON.stringify(results));
```

The `scrape_tiktoks(n_to_scrape, delay)` function has two arguments; the `n_to_scrape` positional argument indicates the number of TikToks whose information will be scraped, while the `delay` keyword argument specifies a number of milliseconds to wait for a single TikTok's information to load before scraping it. In practice, I have found that using my home WiFi and using a premium VPN, 2000 ms tends to be sufficient for most videos; occasionally, the comments will take longer to load and will thus not be scraped, but 2000 ms strikes a good balance between speed and performance.

Once the call of `scrape_tiktoks` has concluded, the JSON-stringified results must be pasted into a json file in the `info/` folder.

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




## Downloading Videos and Covers

No connection adapters were found for 'blob:https://www.tiktok.com/8ae6f5dd-a481-4f06-a57d-76c7b35b4a2b'

HTTPSConnectionPool(host='v19-webapp-prime.us.tiktok.com', port=443): Max retries exceeded with url: /video/tos/useast5/tos-useast5-ve-0068c004-tx/fd0cb2fe060a4d63886ecb79be3bf4c2/?a=1988&ch=0&cr=0&dr=0&lr=tiktok_m&cd=0%7C0%7C1%7C0&cv=1&br=5078&bt=2539&cs=0&ds=3&ft=ebLH6H-qMyq8ZURx9he2Nbiufl7Gb&mime_type=video_mp4&qs=0&rc=aTczPGk1NzQ1OjNlNmQ8NUBpamxkOWc6ZmtzPDMzZzczNEAuLzEvM2MzNS4xX18yMTRhYSNoMGdocjRva25gLS1kMS9zcw%3D%3D&expire=1669992319&l=202212020843558660FE8A6C7290012B92&policy=2&signature=76460e600b74344c413e5563432e9521&tk=tt_chain_token (Caused by SSLError(CertificateError("hostname 'v19-webapp-prime.us.tiktok.com' doesn't match either of '*.hypstarcdn.com', 'hypstarcdn.com'")))


## Optical Character Recognition

The open source Tesseract OCR engine (v5.2.0.20220712) is used to extract text from cover photos. The script `data/ocr.py` uses the `pytesseract` library (v0.3.10), which provides a Python-based interface for Tesseract, to extract text from all of the cover photos whose TikTok ids are present in `data/master.json` and whose corresponding files (`{id}.jpg`) are present in `data/coverphotos`. Results are saved as (id,recognized_string) pairs in `data/ocr.json`.

Note: because `data/downloader.py` also logs information for TikToks that were unable to be downloaded, `data/ocr.py` skips any id for which there is not a corresponding file in `data/coverphotos`. Additionally, some photos are corrupted and raise a `PIL.UnidentifiedImageError` when attempting to load them. For these, we simply continue, assigning the ID to `NULL` (`None`) in `data/ocr.json`.


## Speech-to-Text



##
