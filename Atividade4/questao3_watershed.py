import os
import json
from collections import deque
import argparse
import numpy as np
from PIL import Image as PILImage
from PIL import Image
from scipy.ndimage import distance_transform_edt, maximum_filter, label

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_gray(path):
    img = PILImage.open(path).convert('L')
    w, h = img.size
    img = img.resize((w//4, h//4), PILImage.Resampling.LANCZOS)
    return np.array(img, dtype=np.float32)

def save_u8(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)

def binarize(img, thresh=128):
    return (img > thresh).astype(np.uint8) * 255

def erode(bin_img, se_size=3):
    se = np.ones((se_size, se_size), dtype=np.uint8)
    h, w = bin_img.shape
    sh, sw = se.shape
    ph, pw = sh//2, sw//2
    pad = np.pad(bin_img, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
    out = np.zeros_like(bin_img, dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            region = pad[i:i+sh, j:j+sw]
            if np.all(region == 255):
                out[i, j] = 255
    return out

def dilate(bin_img, se_size=3):
    se = np.ones((se_size, se_size), dtype=np.uint8)
    h, w = bin_img.shape
    sh, sw = se.shape
    ph, pw = sh//2, sw//2
    pad = np.pad(bin_img, ((ph, ph), (pw, pw)), mode='constant', constant_values=0)
    out = np.zeros_like(bin_img, dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            region = pad[i:i+sh, j:j+sw]
            if np.any(region == 255):
                out[i, j] = 255
    return out

def opening(bin_img, se_size=3):
    return dilate(erode(bin_img, se_size), se_size)

def closing(bin_img, se_size=3):
    return erode(dilate(bin_img, se_size), se_size)

def find_markers(dist_img, threshold=0.5):
    max_local = maximum_filter(dist_img, size=3, mode='constant', cval=0)
    is_max = (dist_img == max_local) & (dist_img > threshold)
    labeled, num = label(is_max)
    return labeled.astype(np.int32), num

def watershed(markers, gradient, connectivity=4):
    h, w = gradient.shape
    label_map = np.copy(markers)
    queue = deque()
    neighbors = [(-1,0),(1,0),(0,-1),(0,1)] if connectivity==4 else [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    for i in range(h):
        for j in range(w):
            if label_map[i, j] > 0:
                queue.append((i, j, label_map[i, j]))

    while queue:
        i, j, lbl = queue.popleft()
        for di, dj in neighbors:
            ni, nj = i+di, j+dj
            if 0 <= ni < h and 0 <= nj < w:
                if label_map[ni, nj] == 0:
                    label_map[ni, nj] = lbl
                    queue.append((ni, nj, lbl))
                elif label_map[ni, nj] != lbl:
                    label_map[ni, nj] = -1
    return label_map

def process_image(img_path, outdir):
    img = load_gray(img_path)
    save_u8(img, os.path.join(outdir, 'original_gray.png'))

    bin_img = binarize(img, 128)
    save_u8(bin_img, os.path.join(outdir, 'binaria.png'))

    clean = opening(bin_img, 3)
    clean = closing(clean, 3)
    save_u8(clean, os.path.join(outdir, 'limpa.png'))

    dist = distance_transform_edt(clean == 255)
    if dist.max() > 0:
        dist = dist / dist.max()
    dist_vis = (dist * 255).astype(np.uint8)
    save_u8(dist_vis, os.path.join(outdir, 'distancia.png'))

    markers, num_markers = find_markers(dist, threshold=0.5)
    markers_vis = np.zeros_like(img, dtype=np.uint8)
    markers_vis[markers > 0] = 255
    save_u8(markers_vis, os.path.join(outdir, 'marcadores.png'))

    gy, gx = np.gradient(img)
    grad_mag = np.sqrt(gx**2 + gy**2)
    if grad_mag.max() > 0:
        grad_mag = grad_mag / grad_mag.max()

    watershed_labels = watershed(markers, grad_mag, connectivity=4)

    ws_vis = np.zeros_like(img, dtype=np.uint8)
    ws_vis[watershed_labels == -1] = 255
    ws_vis[watershed_labels > 0] = 128
    save_u8(ws_vis, os.path.join(outdir, 'watershed_resultado.png'))

    overlay = img.copy()
    overlay[watershed_labels == -1] = 255
    save_u8(overlay, os.path.join(outdir, 'segmentacao_overlay.png'))

    return {
        'num_markers': int(num_markers),
        'num_regions': len(np.unique(watershed_labels)) - 1
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    ensure_dir(args.outdir)
    results = process_image(args.input, args.outdir)

    json_path = os.path.join(args.outdir, 'resultados_q3.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()