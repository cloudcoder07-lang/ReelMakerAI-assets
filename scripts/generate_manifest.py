import os
import json

# CONFIG — update this with your GitHub username and repo name
GITHUB_USER = "cloudcoder07-lang"
REPO_NAME = "ReelMakerAI-assets"
BRANCH = "main"
ASSET_FOLDER = "../luts"  # relative to script location

def get_file_size_kb(path):
    size_bytes = os.path.getsize(path)
    return f"{round(size_bytes / 1024)}KB"

def build_cdn_url(filename):
    return f"https://cdn.jsdelivr.net/gh/{GITHUB_USER}/{REPO_NAME}@{BRANCH}/luts/{filename}"

def generate_manifest():
    manifest = {"luts": []}
    for filename in os.listdir(ASSET_FOLDER):
        if filename.endswith(".cube"):
            file_path = os.path.join(ASSET_FOLDER, filename)
            entry = {
                "name": os.path.splitext(filename)[0].replace("_", " ").title(),
                "type": "remote",
                "url": build_cdn_url(filename),
                "size": get_file_size_kb(file_path),
                "mood": "Unknown"  # You can manually update this later
            }
            manifest["luts"].append(entry)

    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("✅ manifest.json generated successfully.")

if __name__ == "__main__":
    generate_manifest()
