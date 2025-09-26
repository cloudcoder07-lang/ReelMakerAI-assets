import os
import json

# CONFIG — update with your GitHub username and repo name
GITHUB_USER = "cloudcoder07-lang"
REPO_NAME = "ReelMakerAI-assets"
BRANCH = "main"

# Asset folders
ASSET_ROOT = "../assets"
MANIFEST_PATH = os.path.join(ASSET_ROOT, "manifest.json")

def get_file_size_kb(path):
    size_bytes = os.path.getsize(path)
    return f"{round(size_bytes / 1024)}KB"

def build_cdn_url(folder, filename):
    return f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@{BRANCH}/assets/{folder}/{filename}"

def scan_folder(folder, extensions, mood_tag="Unknown"):
    folder_path = os.path.join(ASSET_ROOT, folder)
    entries = []

    for filename in os.listdir(folder_path):
        if any(filename.lower().endswith(ext) for ext in extensions):
            file_path = os.path.join(folder_path, filename)
            entry = {
                "name": os.path.splitext(filename)[0].replace("_", " ").title(),
                "type": "remote",
                "url": build_cdn_url(folder, filename),
                "size": get_file_size_kb(file_path),
                "mood": mood_tag
            }

            # Add thumbnail if available
            thumb_path = os.path.join(ASSET_ROOT, "thumbnails", f"{os.path.splitext(filename)[0]}.jpg")
            if os.path.exists(thumb_path):
                entry["preview"] = build_cdn_url("thumbnails", f"{os.path.splitext(filename)[0]}.jpg")

            entries.append(entry)

    return entries

def generate_manifest():
    manifest = {
        "luts": scan_folder("luts", [".cube"]),
        "fonts": scan_folder("fonts", [".ttf", ".otf"]),
        "stickers": scan_folder("stickers", [".png", ".svg"])
    }

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"✅ Manifest written to {MANIFEST_PATH}")

if __name__ == "__main__":
    generate_manifest()
