import requests
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


def download_tiktoks_from_info(json_info_filepath):
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

    for (i,tiktok) in enumerate(info):
        print(f"Downloading {i+1} / {len(info)}")
        try:
            download_file(tiktok["video-src"],f'videos/{tiktok["id"]}.mp4')
            download_file(tiktok["coverphoto-src"],f'coverphotos/{tiktok["id"]}.jpg')
            tiktok["download-timestamp"] = time.time()
            #Log the timestamp of us downloading the TikTok.
        except requests.exceptions.InvalidSchema:
            print("Error!")
            tiktok["download-timestamp"] = None
            #If the download failed, we'll keep the data in our records, but
            #indicate that the download is missing with a NULL value for the
            #download-timestamp.

        master.append(tiktok)

    with open("master.json","w",encoding="utf-8") as f:
        json.dump(master, f, indent=4)


if __name__ == "__main__":
    download_tiktoks_from_info("info/test.json")
