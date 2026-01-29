import os
import requests
import hashlib

rssUrl = "https://angloco.exblog.jp/index.xml"
discordUrl = os.environ["DISCORD_WBHOOK_URL"]
digestFile = "blogHash.txt"

r = requests.get(rssUrl, timeout=10)
r.raise_for_status()
digest = hashlib.sha256(r.content).hexdigest()

try:
    with open(digestFile, "r") as f:
        existingHash = f.read().strip()

except FileNotFoundError:
    existingHash = ""

if (digest != existingHash):
    msg = {"content": "New blog update detected - https://angloco.exblog.jp"}
    resp = requests.post(discordUrl, json=msg, timeout=10)
    resp.raise_for_status()

    with open(digestFile, "w") as f:
        f.write(digest + "\n")
