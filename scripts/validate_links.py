import json
import requests
import os

# Path to your manifest file
MANIFEST_PATH = "../assets/luts/manifest.json"

def validate_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def validate_manifest_links():
    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Manifest not found at {MANIFEST_PATH}")
        return

    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    broken = []
    for entry in manifest.get("luts", []):
        url = entry.get("url")
        name = entry.get("name")
        print(f"🔍 Checking {name} → {url}")
        if validate_url(url):
            print("✅ OK")
        else:
            print("❌ Broken")
            broken.append((name, url))

    if broken:
        print("\n🚨 Broken Links Found:")
        for name, url in broken:
            print(f"- {name}: {url}")
    else:
        print("\n🎉 All links are valid!")

if __name__ == "__main__":
    validate_manifest_links()
