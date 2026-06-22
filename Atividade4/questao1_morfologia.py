import os
import json
import argparse
import numpy as np
from PIL import Image

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_image(path, mode='L'):
    return np.array(Image.open(path).convert(mode), dtype=np.uint8)

def save_image(arr, path):
    Image.fromarray(arr).save(path)

def binarize(img, threshold=128):
    return (img > threshold).astype(np.uint8) * 255

def get_struct_elem(size):
    return np.ones((size, size), dtype=np.uint8)

def erode(bin_img, se):
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

def dilate(bin_img, se):
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

def opening(bin_img, se):
    return dilate(erode(bin_img, se), se)

def closing(bin_img, se):
    return erode(dilate(bin_img, se), se)

def process_image(img_path, outdir, se_sizes=[3,5,15]):
    name = os.path.splitext(os.path.basename(img_path))[0]
    img = load_image(img_path, 'L')
    bin_img = binarize(img, 128)
    save_image(bin_img, os.path.join(outdir, f'{name}_binaria.png'))

    results = {}
    for size in se_sizes:
        se = get_struct_elem(size)
        eroded = erode(bin_img, se)
        dilated = dilate(bin_img, se)
        opened = opening(bin_img, se)
        closed = closing(bin_img, se)

        save_image(eroded, os.path.join(outdir, f'{name}_erodido_{size}.png'))
        save_image(dilated, os.path.join(outdir, f'{name}_dilatado_{size}.png'))
        save_image(opened, os.path.join(outdir, f'{name}_abertura_{size}.png'))
        save_image(closed, os.path.join(outdir, f'{name}_fechamento_{size}.png'))

        results[f'se_{size}'] = {
            'eroded': os.path.join(outdir, f'{name}_erodido_{size}.png'),
            'dilated': os.path.join(outdir, f'{name}_dilatado_{size}.png'),
            'opened': os.path.join(outdir, f'{name}_abertura_{size}.png'),
            'closed': os.path.join(outdir, f'{name}_fechamento_{size}.png'),
        }
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', nargs='+', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    ensure_dir(args.outdir)
    all_results = {}
    for path in args.inputs:
        all_results[os.path.basename(path)] = process_image(path, args.outdir)

    json_path = os.path.join(args.outdir, 'resultados_q1.json')
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2)

if __name__ == '__main__':
    main()