from PIL import Image, UnidentifiedImageError
import pytesseract
import numpy as np
import json
import time
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#Have to manually set the path because Windows sucks.

print("Loading JSON data...")
start = time.time()
with open("master.json","r",encoding="utf-8") as f:
    master_text = f.read()
tiktoks = json.loads(master_text)
print(f"Completed in {time.time()-start:.2f} seconds.\n")

ocr_results = {}

print("Performing OCR on cover photos...")
start = time.time()
for (i,(id,tiktok)) in enumerate(tiktoks.items()):
    print(f"Extracting text {i+1} / {len(tiktoks)}")
    if (tiktok["download-timestamp"] == None) and not (os.path.isfile(f"coverphotos/{id}.jpg")):
        print("File not downloaded.")
        continue

    try:
        img = np.array(Image.open(f"coverphotos/{id}.jpg"))
        ocr_results[id] = pytesseract.image_to_string(img)
    except UnidentifiedImageError:
        ocr_results[id] = None
        print(f"Broken image: {id}")


print(f"Completed in {time.time()-start:.2f} seconds.\n")



print("Saving results...")
start = time.time()
with open("ocr.json","w",encoding="utf-8") as f:
    json.dump(ocr_results, f, indent=4)
print(f"Completed in {time.time()-start:.2f} seconds.\n")
