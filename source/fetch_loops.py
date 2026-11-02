#!/usr/bin/env python3
"""Downloads the Seedance 2.5 loops for the Lumavu website into Website/_media/raw/.
Run from anywhere:  python3 "/Volumes/T7 RED 500/App - Lumavu/Website/source/fetch_loops.py"
"""
import os, urllib.request
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3Ix9Ekh28iyal5WyfdPc46ycf26/"
LOOPS = {
    "news": "hf_20261025_072420_9723b594-e596-49c7-b716-861fd1455858.mp4",
    "football": "hf_20261025_072427_c7c055b6-7d52-43f8-9181-db8b4f4d731f.mp4",
    "leopard": "hf_20261025_072420_a5842fe1-a611-423a-95f3-767563ac894d.mp4",
    "motorsport": "hf_20261025_072419_d631096b-fc96-4ad9-9c82-0d35215e741d.mp4",
    "dunes": "hf_20261025_072420_585654f8-0ada-484e-aa45-31a62917a7a0.mp4",
    # the hero is two shots cut together: the caravan walking, then a wider shot
    "salt-road-walk": "hf_20261025_111037_e5505ed3-52aa-44b9-80b9-5c183dc5026a.mp4",
    "salt-road-aerial": "hf_20261025_113917_b00db66c-24c6-4e60-9c22-4f66e853c5b9.mp4",
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_media", "raw")
os.makedirs(out, exist_ok=True)
for key, name in LOOPS.items():
    dest = os.path.join(out, key + ".mp4")
    if os.path.exists(dest) and os.path.getsize(dest) > 200000:
        print("have", key); continue
    if not name.endswith(".mp4"):
        print("not ready yet", key); continue
    urllib.request.urlretrieve(BASE + name, dest)
    print("saved", key, os.path.getsize(dest) // 1024, "KB")
print("Done. Tell Claude the loops are in.")
