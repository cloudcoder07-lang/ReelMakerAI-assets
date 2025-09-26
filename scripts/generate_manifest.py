import os
import json

# CONFIG — update with your GitHub username and repo name
GITHUB_USER = "cloudcoder07-lang"
REPO_NAME = "ReelMakerAI-assets"
BRANCH = "main"

# Folder paths relative to this script
LUT_FOLDER = "../assets/luts"
MANIFEST_PATH = os.path.join(LUT_FOLDER, "manifest.json")

def get_file_size_kb(path):
    size_bytes = os.path.getsize(path)
    return f"{round(size_bytes / 1024)}KB"

def build_cdn_url(filename):
    return f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@{BRANCH}/assets/luts/{filename}"

def generate_manifest():
    manifest = {"luts": []}

    if not os.path.exists(LUT_FOLDER):
        print(f"❌ LUT folder not found: {LUT_FOLDER}")
        return

    for filename in os.listdir(LUT_FOLDER):
        if filename.endswith(".cube"):
            file_path = os.path.join(LUT_FOLDER, filename)
            entry = {
                "name": os.path.splitext(filename)[0].replace("_", " ").title(),
                "type": "remote",
                "url": build_cdn_url(filename),
                "size": get_file_size_kb(file_path),
                "mood": "Unknown"  # You can manually update this later
            }
            manifest["luts"].append(entry)

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"✅ Manifest written to {MANIFEST_PATH}")

if __name__ == "__main__":
    generate_manifest()
