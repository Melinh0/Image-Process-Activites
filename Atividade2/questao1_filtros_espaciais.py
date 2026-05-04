import os
import json
from math import exp
import numpy as np
from PIL import Image

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_gray(path):
    img = Image.open(path).convert('L')
    return np.array(img, dtype=np.float32)

def save_u8(arr, path):
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)

def pad_image(img, ph, pw, mode='reflect'):
    if mode == 'zero':
        padded = np.zeros((img.shape[0]+2*ph, img.shape[1]+2*pw), dtype=img.dtype)
        padded[ph:ph+img.shape[0], pw:pw+img.shape[1]] = img
        return padded
    return np.pad(img, ((ph,ph),(pw,pw)), mode='reflect')

def convolve2d(img, kernel, pad_mode='reflect'):
    kh, kw = kernel.shape
    ph, pw = kh//2, kw//2
    padded = pad_image(img, ph, pw, pad_mode)
    out = np.zeros_like(img, dtype=np.float32)
    k = np.flip(np.flip(kernel, axis=0), axis=1)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            out[y,x] = np.sum(padded[y:y+kh, x:x+kw] * k)
    return out

def gaussian_kernel(size, sigma):
    ax = np.arange(-size//2+1., size//2+1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2+yy**2)/(2.*sigma**2))
    return kernel / np.sum(kernel)

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--outdir', default='atividade2/saidas/saidas_questao2')
    args = p.parse_args()

    ensure_dir(args.outdir)
    img = load_gray(args.input)

    kernels = {}
    kernels['h1'] = np.ones((3,3), dtype=np.float32)/9.0
    kernels['h2'] = gaussian_kernel(5, 1.0)
    kernels['h3'] = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)
    kernels['h4'] = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32)
    kernels['h5'] = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=np.float32)
    kernels['h6'] = np.array([[-1,-1,-1],[0,0,0],[1,1,1]], dtype=np.float32)
    kernels['h7'] = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]], dtype=np.float32)
    kernels['h8'] = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], dtype=np.float32)
    kernels['h9'] = np.array([[-2,-1,0],[-1,1,1],[0,1,2]], dtype=np.float32)
    kernels['h10'] = np.ones((5,5), dtype=np.float32)/25.0
    g5 = gaussian_kernel(5, 1.0)
    delta = np.zeros((5,5), dtype=np.float32)
    delta[2,2] = 1.0
    kernels['h11'] = delta + 1.0*(delta - g5)

    results = {}
    for name, k in kernels.items():
        out = convolve2d(img, k)
        minv, maxv = out.min(), out.max()
        if maxv > minv:
            out_vis = (out - minv) * (255.0/(maxv - minv))
        else:
            out_vis = np.clip(out, 0, 255)
        out_path = os.path.join(args.outdir, f'q1_{name}.png')
        save_u8(out_vis, out_path)
        results[name] = {
            'kernel_shape': list(k.shape),
            'min': float(minv),
            'max': float(maxv),
            'mean': float(np.mean(out)),
            'image': out_path
        }
    json_path = os.path.join(args.outdir, 'resultados_q1.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'Filtros espaciais salvos em {args.outdir}')

if __name__ == '__main__':
    main()