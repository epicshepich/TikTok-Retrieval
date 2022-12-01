import requests
import json

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
    with open(json_info_filepath, "r",encoding="utf-8") as f:
        info_text = f.read()
    info = json.loads(info_text)
    errors = []
    for tiktok in info:
        try:
            download_file(tiktok["video-src"],f'videos/{tiktok["id"]}.mp4')
            download_file(tiktok["coverphoto-src"],f'coverphotos/{tiktok["id"]}.jpg')
        except requests.exceptions.InvalidSchema:
            errors.append(tiktok["id"])


if __name__ == "__main__":
    download_tiktoks_from_info("info/test.json")
