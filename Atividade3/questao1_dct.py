import os
import json
import math
import numpy as np
from PIL import Image

BLOCK_SIZE = 8

QUANT_MATRIX = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68,109,103, 77],
    [24, 35, 55, 64, 81,104,113, 92],
    [49, 64, 78, 87,103,121,120,101],
    [72, 92, 95, 98,112,100,103, 99],
], dtype=np.float32)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_gray(path):
    return np.array(Image.open(path).convert('L'), dtype=np.float32)


def save_u8(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)


def dct2d(block):
    N = BLOCK_SIZE
    result = np.zeros((N, N), dtype=np.float64)
    for u in range(N):
        for v in range(N):
            cu = 1.0 / math.sqrt(2) if u == 0 else 1.0
            cv = 1.0 / math.sqrt(2) if v == 0 else 1.0
            s = 0.0
            for x in range(N):
                for y in range(N):
                    s += (block[x, y] *
                          math.cos((2*x + 1)*u*math.pi / (2*N)) *
                          math.cos((2*y + 1)*v*math.pi / (2*N)))
            result[u, v] = (2.0 / N) * cu * cv * s
    return result


def idct2d(block):
    N = BLOCK_SIZE
    result = np.zeros((N, N), dtype=np.float64)
    for x in range(N):
        for y in range(N):
            s = 0.0
            for u in range(N):
                for v in range(N):
                    cu = 1.0 / math.sqrt(2) if u == 0 else 1.0
                    cv = 1.0 / math.sqrt(2) if v == 0 else 1.0
                    s += (cu * cv * block[u, v] *
                          math.cos((2*x + 1)*u*math.pi / (2*N)) *
                          math.cos((2*y + 1)*v*math.pi / (2*N)))
            result[x, y] = (2.0 / N) * s
    return result


def quantize_block(dct_block, q_scale=1.0):
    scaled_q = QUANT_MATRIX * q_scale
    return np.round(dct_block / scaled_q)


def dequantize_block(quant_block, q_scale=1.0):
    scaled_q = QUANT_MATRIX * q_scale
    return quant_block * scaled_q


def process_image(gray, q_scale=1.0):
    h, w = gray.shape
    bh = (h // BLOCK_SIZE) * BLOCK_SIZE
    bw = (w // BLOCK_SIZE) * BLOCK_SIZE
    img = gray[:bh, :bw]
    reconstructed = np.zeros_like(img, dtype=np.float64)
    for i in range(0, bh, BLOCK_SIZE):
        for j in range(0, bw, BLOCK_SIZE):
            block = img[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE].astype(np.float64) - 128.0
            dct = dct2d(block)
            quant = quantize_block(dct, q_scale)
            dequant = dequantize_block(quant, q_scale)
            idct = idct2d(dequant)
            reconstructed[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE] = idct + 128.0
    return img, np.clip(reconstructed, 0, 255)


def psnr(original, reconstructed):
    mse = np.mean((original.astype(np.float64) - reconstructed.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    return 10.0 * math.log10(255.0**2 / mse)


def mean_absolute_error(original, reconstructed):
    return float(np.mean(np.abs(original.astype(np.float64) - reconstructed.astype(np.float64))))


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--outdir', default='Atividade3/resultados_q1')
    args = p.parse_args()

    ensure_dir(args.outdir)

    gray = load_gray(args.input)
    save_u8(gray, os.path.join(args.outdir, 'original_gray.png'))

    q_scales = [0.5, 1.0, 2.0, 4.0, 8.0]
    results = {}

    for qs in q_scales:
        original_crop, reconstructed = process_image(gray, q_scale=qs)
        tag = str(qs).replace('.', '_')
        out_path = os.path.join(args.outdir, f'reconstruida_q{tag}.png')
        save_u8(reconstructed, out_path)

        diff = np.abs(original_crop.astype(np.float64) - reconstructed)
        diff_norm = diff / diff.max() * 255.0 if diff.max() > 0 else diff
        diff_path = os.path.join(args.outdir, f'diferenca_q{tag}.png')
        save_u8(diff_norm, diff_path)

        psnr_val = psnr(original_crop, reconstructed)
        mae_val = mean_absolute_error(original_crop, reconstructed)

        results[tag] = {
            'q_scale': qs,
            'psnr': round(psnr_val, 4),
            'mae': round(mae_val, 4),
            'reconstructed': out_path,
            'diff': diff_path
        }
        print(f'q_scale={qs} | PSNR={psnr_val:.2f} dB | MAE={mae_val:.2f}')

    json_path = os.path.join(args.outdir, 'resultados_q1.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f'\nResultados salvos em {args.outdir}')


if __name__ == '__main__':
    main()