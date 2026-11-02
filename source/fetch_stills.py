#!/usr/bin/env python3
"""Downloads the 20 Higgsfield stills for the Lumavu website into Website/_media/raw/.
Run from anywhere:  python3 "/Volumes/T7 RED 500/App - Lumavu/Website/source/fetch_stills.py"
"""
import os, urllib.request
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3Ix9Ekh28iyal5WyfdPc46ycf26/"
STILLS = {
    "salt-road": "hf_20261024_222553_17ac2607-f692-4e5b-91cf-b6b9a7ae8da3.png",
    "glass-harbour": "hf_20261024_222553_119a211d-3b04-4834-aa7d-38c214aedb81.png",
    "northern-quiet": "hf_20261024_222554_8793d16e-305a-4a5f-8a91-86a6d35e1bad.png",
    "orbit-nine": "hf_20261024_222555_1431d6e4-1546-40e7-86cf-56746abb5920.png",
    "midnight-souk": "hf_20261024_222553_761647b0-4b25-4bac-a268-fe43ca819339.png",
    "ember-coast": "hf_20261024_222553_b6619abe-a1ca-4993-854f-61760023a906.png",
    "saffron": "hf_20261024_222553_a267e9f0-ab06-4514-817a-a059f2daac75.png",
    "kingdom-of-glass": "hf_20261024_222554_1dbf35d9-b911-49b2-b6e8-5a620731b2ea.png",
    "lanterns": "hf_20261024_222554_60107f9e-66a0-456a-95ee-9272b8e9d34f.png",
    "paper-moons": "hf_20261024_222554_763f7db9-c3da-4ecc-99ed-e890bb6f47c2.png",
    "news": "hf_20261024_222551_fa3c528a-7afd-41e4-acfd-3f901ad7b0d7.png",
    "football": "hf_20261024_222555_aee9b78a-d8a3-4140-a5cd-5861757d720b.png",
    "dunes": "hf_20261024_222601_5cf67b39-f424-4d16-b3cf-71af46fc8d67.png",
    "earth": "hf_20261024_222601_79213208-041d-4923-adff-3174d989238a.png",
    "concert": "hf_20261024_222600_6a771f32-6f55-47e3-a803-760af3105947.png",
    "kids": "hf_20261024_222602_e3e2e359-6976-4e41-8fff-2b78936d0350.png",
    "farmhouse": "hf_20261024_222600_a7884e7c-de90-4d11-b576-6c6fd02abcf2.png",
    "undertow": "hf_20261024_222601_a0d63ad8-1fca-46b1-a830-559f5e8fc2ef.png",
    "leopard": "hf_20261024_222600_45aa3776-b728-4ec7-8c30-f02bc042569e.png",
    "motorsport": "hf_20261024_222601_f0c5811c-b9ca-4687-a557-fc1802986e3f.png",
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_media", "raw")
os.makedirs(out, exist_ok=True)
for key, name in STILLS.items():
    dest = os.path.join(out, key + ".png")
    if os.path.exists(dest) and os.path.getsize(dest) > 100000:
        print("have", key); continue
    urllib.request.urlretrieve(BASE + name, dest)
    print("saved", key, os.path.getsize(dest) // 1024, "KB")
print("Done. Tell Claude the stills are in.")
