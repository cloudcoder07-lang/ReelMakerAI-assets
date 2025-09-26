import os
import cv2
import numpy as np

# Paths
LUT_FOLDER = "../assets/luts"
THUMBNAIL_FOLDER = "../assets/thumbnails"

# Ensure output folder exists
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

def load_cube_lut(path):
    with open(path, "r") as f:
        lines = f.readlines()

    lut_data = []
    for line in lines:
        if line.strip() and not line.startswith("#") and not line.startswith("TITLE") and not line.startswith("LUT_3D_SIZE"):
            parts = line.strip().split()
            if len(parts) == 3:
                lut_data.append([float(p) for p in parts])

    lut = np.array(lut_data)
    size = int(round(lut.shape[0] ** (1/3)))
    return lut.reshape((size, size, size, 3)), size

def generate_gradient_image(size=256):
    gradient = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            val = int((x + y) / (2 * size) * 255)
            gradient[y, x] = (val, val, val)
    return gradient

def apply_lut(image, lut, size):
    img = image.astype(np.float32) / 255.0
    r = (img[:, :, 2] * (size - 1)).astype(np.int32)
    g = (img[:, :, 1] * (size - 1)).astype(np.int32)
    b = (img[:, :, 0] * (size - 1)).astype(np.int32)
    mapped = lut[r, g, b]
    mapped = (mapped * 255).astype(np.uint8)
    return mapped

def generate_thumbnails():
    base_image = generate_gradient_image()

    for filename in os.listdir(LUT_FOLDER):
        if filename.endswith(".cube"):
            lut_path = os.path.join(LUT_FOLDER, filename)
            try:
                lut, size = load_cube_lut(lut_path)
                thumb = apply_lut(base_image, lut, size)
                out_path = os.path.join(THUMBNAIL_FOLDER, f"{os.path.splitext(filename)[0]}.jpg")
                cv2.imwrite(out_path, thumb)
                print(f"✅ Generated thumbnail: {out_path}")
            except Exception as e:
                print(f"❌ Failed for {filename}: {e}")

if __name__ == "__main__":
    generate_thumbnails()
