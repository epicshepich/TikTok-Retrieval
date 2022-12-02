import json

with open("master.json","r",encoding="utf-8") as f:
    master_text = f.read()
master_list = json.loads(master_text)

master_dict = {}
for tiktok in master_list:
    master_dict[tiktok["id"]] = tiktok

with open("master_dict.json","w",encoding="utf-8") as f:
    json.dump(master_dict, f, indent=4)
