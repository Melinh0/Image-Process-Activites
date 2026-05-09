import argparse
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def ensure_dir(path): os.makedirs(path, exist_ok=True)

def load_gray_float(path):
    return np.array(Image.open(path).convert("L"), dtype=np.float32)

def save_u8(arr, path):
    Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).save(path)

def minmax_to_uint8(arr):
    arr = np.asarray(arr, dtype=np.float32)
    mn, mx = arr.min(), arr.max()
    if mx <= mn: return np.zeros_like(arr, dtype=np.uint8)
    norm = (arr - mn) * (255.0/(mx - mn))
    return np.clip(norm, 0, 255).astype(np.uint8)

def freq_grid(shape):
    rows, cols = shape
    crow, ccol = rows//2, cols//2
    u = np.arange(rows)
    v = np.arange(cols)
    U, V = np.meshgrid(u, v, indexing="ij")
    return np.sqrt((U-crow)**2 + (V-ccol)**2)

def lowpass_mask(D, r): return (D <= r).astype(np.float32)
def highpass_mask(D, r): return (D > r).astype(np.float32)
def bandpass_mask(D, r1, r2): return ((D >= r1) & (D <= r2)).astype(np.float32)
def bandreject_mask(D, r1, r2): return 1.0 - bandpass_mask(D, r1, r2)

def spectrum_log_uint8(F_shift):
    return minmax_to_uint8(np.log1p(np.abs(F_shift)))

def apply_filter(F_shift, mask):
    G_shift = F_shift * mask
    g_real = np.real(np.fft.ifft2(np.fft.ifftshift(G_shift)))
    return minmax_to_uint8(g_real), spectrum_log_uint8(G_shift)

def compress_by_percentile(F_shift, pctl):
    mag = np.abs(F_shift)
    thr = np.percentile(mag, pctl)
    keep = mag >= thr
    F_comp = F_shift * keep
    g_real = np.real(np.fft.ifft2(np.fft.ifftshift(F_comp)))
    total = keep.size
    kept = np.count_nonzero(keep)
    return minmax_to_uint8(g_real), {
        "percentil": pctl,
        "limiar": float(thr),
        "coeficientes_totais": total,
        "coeficientes_mantidos": int(kept),
        "taxa_zerados": float(total - kept)/total
    }

def save_histogram(img, path, title):
    plt.figure(figsize=(8,4.2))
    plt.hist(img.ravel(), bins=256, range=(0,255), color="#2368B5")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

def save_hist_comparison(original, comp_imgs, path):
    plt.figure(figsize=(9.5,5))
    hist_o, bins = np.histogram(original.ravel(), bins=256, range=(0,255))
    centers = (bins[:-1]+bins[1:])/2.0
    plt.plot(centers, hist_o, label="Original", linewidth=2)
    for label, img in comp_imgs.items():
        hist_c, _ = np.histogram(img.ravel(), bins=256, range=(0,255))
        plt.plot(centers, hist_c, label=f"Comprimida {label}", linewidth=1.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--outdir", default="atividade2/saidas/saidas_questao2")
    p.add_argument("--low-high-radii", default="15,30,60")
    p.add_argument("--band-pairs", default="10-30,20-50")
    p.add_argument("--compress-thresholds", default="70,85,95")
    args = p.parse_args()

    radii = [int(x.strip()) for x in args.low_high_radii.split(",")]
    band_pairs = []
    for pr in args.band_pairs.split(","):
        r1,r2 = map(int, pr.strip().split("-"))
        band_pairs.append((r1,r2))
    comp_pct = [int(x.strip()) for x in args.compress_thresholds.split(",")]

    ensure_dir(args.outdir)
    sub = lambda d: os.path.join(args.outdir, d)
    for d in ["00_fft","01_masks","02_filtradas","03_compressao","04_histogramas"]:
        ensure_dir(sub(d))

    img = load_gray_float(args.input)
    img_u8 = np.clip(img,0,255).astype(np.uint8)
    F = np.fft.fft2(img)
    F_shift = np.fft.fftshift(F)
    spec_orig = spectrum_log_uint8(F_shift)
    save_u8(spec_orig, sub("00_fft/fft_espectro_centralizado.png"))

    D = freq_grid(img.shape)
    results_filters = []

    for r in radii:
        lp_mask = lowpass_mask(D, r)
        save_u8((lp_mask*255).astype(np.uint8), sub(f"01_masks/mask_passabaixa_r{r}.png"))
        lp_img, lp_spec = apply_filter(F_shift, lp_mask)
        save_u8(lp_img, sub(f"02_filtradas/filtro_passabaixa_r{r}.png"))
        save_u8(lp_spec, sub(f"02_filtradas/espectro_passabaixa_r{r}.png"))
        results_filters.append(("passa-baixa", f"r={r}", lp_img))

        hp_mask = highpass_mask(D, r)
        save_u8((hp_mask*255).astype(np.uint8), sub(f"01_masks/mask_passaalta_r{r}.png"))
        hp_img, hp_spec = apply_filter(F_shift, hp_mask)
        save_u8(hp_img, sub(f"02_filtradas/filtro_passaalta_r{r}.png"))
        save_u8(hp_spec, sub(f"02_filtradas/espectro_passaalta_r{r}.png"))
        results_filters.append(("passa-alta", f"r={r}", hp_img))

    for r1,r2 in band_pairs:
        bp_mask = bandpass_mask(D, r1, r2)
        save_u8((bp_mask*255).astype(np.uint8), sub(f"01_masks/mask_passafaixa_r{r1}_{r2}.png"))
        bp_img, bp_spec = apply_filter(F_shift, bp_mask)
        save_u8(bp_img, sub(f"02_filtradas/filtro_passafaixa_r{r1}_{r2}.png"))
        save_u8(bp_spec, sub(f"02_filtradas/espectro_passafaixa_r{r1}_{r2}.png"))
        results_filters.append(("passa-faixa", f"r1={r1},r2={r2}", bp_img))

        br_mask = bandreject_mask(D, r1, r2)
        save_u8((br_mask*255).astype(np.uint8), sub(f"01_masks/mask_rejeitafaixa_r{r1}_{r2}.png"))
        br_img, br_spec = apply_filter(F_shift, br_mask)
        save_u8(br_img, sub(f"02_filtradas/filtro_rejeitafaixa_r{r1}_{r2}.png"))
        save_u8(br_spec, sub(f"02_filtradas/espectro_rejeitafaixa_r{r1}_{r2}.png"))
        results_filters.append(("rejeita-faixa", f"r1={r1},r2={r2}", br_img))

    comp_imgs = {}
    comp_stats = []
    for pctl in comp_pct:
        comp_img, stats = compress_by_percentile(F_shift, pctl)
        path = sub(f"03_compressao/compressao_percentil_{pctl}.png")
        save_u8(comp_img, path)
        comp_imgs[f"p{pctl}"] = comp_img
        comp_stats.append({**stats, "image": path})

    save_histogram(img_u8, sub("04_histogramas/histograma_original.png"), "Original")
    for label, cimg in comp_imgs.items():
        save_histogram(cimg, sub(f"04_histogramas/histograma_{label}.png"), f"Comprimida {label}")
    save_hist_comparison(img_u8, comp_imgs, sub("04_histogramas/comparativo_histogramas.png"))

    payload = {
        "input": os.path.abspath(args.input),
        "outdir": os.path.abspath(args.outdir),
        "parametros": {"low_high_radii": radii, "band_pairs": band_pairs, "compress_thresholds": comp_pct},
        "filtros": [{"tipo": t, "parametro": param} for t,param,_ in results_filters],
        "compressao": comp_stats
    }
    with open(os.path.join(args.outdir, "resultados_questao2.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Processamento finalizado. Saídas em {args.outdir}")

if __name__ == "__main__":
    main()