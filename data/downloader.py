import requests
import http
import json
import time

def download_file(url,filename):
    """Shamelessly copied from https://stackoverflow.com/questions/53196594/web-scraping-videos"""
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return filename


def download_tiktoks_from_info(json_info_filepath, retry_missing=False,
    bugged_indices_that_randomly_take_forever={}):
    """Uses `download_file` to download videos and coverphotos corresponding to
    TikToks whose info is scraped into the `json_info_filepath`. Includes error
    handling for `blob:` links, and logs successful results with timestap of download."""
    with open(json_info_filepath,"r",encoding="utf-8") as f:
        info_text = f.read()
    info = json.loads(info_text)

    with open("master.json","r",encoding="utf-8") as f:
        master_text = f.read()
    master = json.loads(master_text)
    #Successful downloads have their info logged to master.json, including a
    #new download-timestamp attribute.
    missing_downloads = set([id for (id,tiktok) in master.items() if tiktok["download-timestamp"] is None])

    for (i,tiktok) in enumerate(info):
        if tiktok["id"] in master:
            if not (retry_missing and tiktok["id"] in missing_downloads):
                continue
            #Skip TikToks that have already been downloaded.
        if i+1 in bugged_indices_that_randomly_take_forever.get(json_info_filepath,[]):
            continue
        print(f"Downloading {i+1} / {len(info)}")
        try:
            download_file(tiktok["video-src"],f'videos/{tiktok["id"]}.mp4')
            download_file(tiktok["coverphoto-src"],f'coverphotos/{tiktok["id"]}.jpg')
            tiktok["download-timestamp"] = time.time()
            #Log the timestamp of us downloading the TikTok.
        except Exception as e:
            print(e)
            tiktok["download-timestamp"] = None
            #If the download failed, we'll keep the data in our records, but
            #indicate that the download is missing with a NULL value for the
            #download-timestamp.

        master[tiktok["id"]] = tiktok

        if (i+1) % 5 == 0:
            with open("master.json","w",encoding="utf-8") as f:
                json.dump(master, f, indent=4)
            #Save info to master every 5 downloads in case something goes wrong.

    with open("master.json","w",encoding="utf-8") as f:
        json.dump(master, f, indent=4)


if __name__ == "__main__":
    download_tiktoks_from_info(
        "info/batch_7.json",
        retry_missing=True,
        bugged_indices_that_randomly_take_forever={
            "info/batch_1":[39],
            "info/batch_2":[184]
        }
    )
