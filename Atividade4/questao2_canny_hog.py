import os
import json
import math
import argparse
import numpy as np
from PIL import Image

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_gray(path):
    return np.array(Image.open(path).convert('L'), dtype=np.float32)

def save_u8(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)

def gaussian_kernel(size, sigma):
    ax = np.arange(-size//2+1, size//2+1)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return kernel / np.sum(kernel)

def convolve(img, kernel):
    kh, kw = kernel.shape
    ph, pw = kh//2, kw//2
    pad = np.pad(img, ((ph, ph), (pw, pw)), mode='reflect')
    out = np.zeros_like(img, dtype=np.float32)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out[i, j] = np.sum(pad[i:i+kh, j:j+kw] * kernel)
    return out

def sobel_kernels():
    Gx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)
    Gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32)
    return Gx, Gy

def gradient_magnitude_orientation(Ix, Iy):
    mag = np.sqrt(Ix**2 + Iy**2)
    orient = np.arctan2(Iy, Ix) * 180 / np.pi
    orient = (orient + 180) % 180
    return mag, orient

def hog_cells(mag, orient, cell_size=8, n_bins=9):
    h, w = mag.shape
    cells_h = h // cell_size
    cells_w = w // cell_size
    hist = np.zeros((cells_h, cells_w, n_bins), dtype=np.float32)
    bin_width = 180.0 / n_bins
    for i in range(cells_h):
        for j in range(cells_w):
            y0 = i * cell_size
            y1 = y0 + cell_size
            x0 = j * cell_size
            x1 = x0 + cell_size
            cell_mag = mag[y0:y1, x0:x1]
            cell_ori = orient[y0:y1, x0:x1]
            for y in range(cell_size):
                for x in range(cell_size):
                    angle = cell_ori[y, x]
                    weight = cell_mag[y, x]
                    if weight == 0:
                        continue
                    bin_idx = int(angle // bin_width)
                    if bin_idx >= n_bins:
                        bin_idx = n_bins - 1
                    hist[i, j, bin_idx] += weight
    return hist

def normalize_hist(hist, eps=1e-5):
    norm = np.sqrt(np.sum(hist**2) + eps**2)
    return hist / norm

def process_image(img_path, outdir, cell_size=8, n_bins=9, gauss_size=5, sigma=1.0):
    img = load_gray(img_path)
    save_u8(img, os.path.join(outdir, 'original.png'))

    kernel = gaussian_kernel(gauss_size, sigma)
    smoothed = convolve(img, kernel)
    save_u8(smoothed, os.path.join(outdir, 'suavizada_gauss.png'))

    Gx, Gy = sobel_kernels()
    Ix = convolve(smoothed, Gx)
    Iy = convolve(smoothed, Gy)
    mag, orient = gradient_magnitude_orientation(Ix, Iy)
    save_u8(mag, os.path.join(outdir, 'magnitude_gradiente.png'))

    mag_vis = (mag / mag.max() * 255).astype(np.uint8)
    save_u8(mag_vis, os.path.join(outdir, 'magnitude_visual.png'))

    hist = hog_cells(mag, orient, cell_size, n_bins)
    hist_norm = normalize_hist(hist.reshape(-1, n_bins))
    hist_norm = hist_norm.reshape(hist.shape)

    vis_hog = np.zeros((mag.shape[0], mag.shape[1]), dtype=np.uint8)
    for i in range(hist.shape[0]):
        for j in range(hist.shape[1]):
            y0 = i * cell_size
            x0 = j * cell_size
            max_val = hist_norm[i, j].max()
            if max_val > 0:
                for b in range(n_bins):
                    ang = b * (180.0 / n_bins) + 90
                    rad = math.radians(ang)
                    length = int(hist_norm[i, j, b] / max_val * cell_size * 0.8)
                    if length < 1:
                        continue
                    cx = x0 + cell_size//2
                    cy = y0 + cell_size//2
                    dx = int(length * math.cos(rad))
                    dy = int(-length * math.sin(rad))
                    for t in range(-1,2):
                        px = cx + dx + t
                        py = cy + dy + t
                        if 0 <= px < mag.shape[1] and 0 <= py < mag.shape[0]:
                            vis_hog[py, px] = 255
    save_u8(vis_hog, os.path.join(outdir, 'hog_visualizacao.png'))

    return {
        'gauss_sigma': sigma,
        'cell_size': cell_size,
        'n_bins': n_bins,
        'histogram_shape': list(hist.shape),
        'hog_features': hist_norm.tolist()
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    ensure_dir(args.outdir)
    results = process_image(args.input, args.outdir)

    json_path = os.path.join(args.outdir, 'resultados_q2.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()