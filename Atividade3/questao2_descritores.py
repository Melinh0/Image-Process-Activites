import os
import json
import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_gray(path):
    return np.array(Image.open(path).convert('L'), dtype=np.float32)


def save_u8(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)


def compute_mean(img):
    return float(np.sum(img) / img.size)


def compute_variance(img, mean):
    return float(np.sum((img - mean) ** 2) / img.size)


def compute_energy(img):
    return float(np.sum(img.astype(np.float64) ** 2) / img.size)


def compute_spatial_variation(img):
    h, w = img.shape
    diff_h = np.abs(img[:, 1:].astype(np.float64) - img[:, :-1].astype(np.float64))
    diff_v = np.abs(img[1:, :].astype(np.float64) - img[:-1, :].astype(np.float64))
    mean_h = float(np.sum(diff_h) / diff_h.size)
    mean_v = float(np.sum(diff_v) / diff_v.size)
    total = float((np.sum(diff_h) + np.sum(diff_v)) / (diff_h.size + diff_v.size))
    return mean_h, mean_v, total


def compute_entropy(img):
    hist = np.zeros(256, dtype=np.float64)
    flat = img.astype(np.uint8).ravel()
    for val in flat:
        hist[val] += 1
    hist /= flat.size
    entropy = 0.0
    for p in hist:
        if p > 0:
            entropy -= p * math.log2(p)
    return float(entropy)


def compute_histogram(img):
    hist = np.zeros(256, dtype=np.int64)
    flat = img.astype(np.uint8).ravel()
    for val in flat:
        hist[val] += 1
    return hist


def describe_image(img):
    mean = compute_mean(img)
    variance = compute_variance(img, mean)
    std = math.sqrt(variance)
    energy = compute_energy(img)
    entropy = compute_entropy(img)
    var_h, var_v, var_total = compute_spatial_variation(img)
    return {
        'mean': round(mean, 4),
        'variance': round(variance, 4),
        'std': round(std, 4),
        'energy': round(energy, 4),
        'entropy': round(entropy, 4),
        'spatial_variation_horizontal': round(var_h, 4),
        'spatial_variation_vertical': round(var_v, 4),
        'spatial_variation_total': round(var_total, 4),
    }


def save_histogram_figure(hist_data, labels, outpath, title='Histogramas Comparativos'):
    fig, axes = plt.subplots(1, len(hist_data), figsize=(6 * len(hist_data), 4))
    if len(hist_data) == 1:
        axes = [axes]
    bins = np.arange(256)
    for ax, hist, label in zip(axes, hist_data, labels):
        ax.bar(bins, hist, width=1, color='steelblue', edgecolor='none')
        ax.set_title(label, fontsize=11)
        ax.set_xlabel('Intensidade')
        ax.set_ylabel('Frequencia')
        ax.set_xlim(0, 255)
    plt.suptitle(title, fontsize=13)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def save_comparison_figure(images, labels, descriptors, outpath):
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 5))
    if n == 1:
        axes = [axes]
    for ax, img, label, desc in zip(axes, images, labels, descriptors):
        ax.imshow(img, cmap='gray', vmin=0, vmax=255)
        ax.set_title(label, fontsize=11)
        info = (
            f"Media: {desc['mean']:.1f}\n"
            f"Var: {desc['variance']:.1f}\n"
            f"Energia: {desc['energy']:.1f}\n"
            f"Entropia: {desc['entropy']:.2f} bits\n"
            f"Var.Espacial: {desc['spatial_variation_total']:.2f}"
        )
        ax.set_xlabel(info, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def save_radar_chart(desc_list, labels, outpath):
    categories = ['Media', 'Std', 'Energia (norm)', 'Entropia', 'Var.Espacial']
    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    colors = ['steelblue', 'coral', 'green', 'purple', 'orange']

    for idx, (desc, label) in enumerate(zip(desc_list, labels)):
        values = [
            desc['mean'] / 255.0,
            desc['std'] / 128.0,
            min(desc['energy'] / 65025.0, 1.0),
            desc['entropy'] / 8.0,
            min(desc['spatial_variation_total'] / 100.0, 1.0)
        ]
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=2,
                color=colors[idx % len(colors)], label=label)
        ax.fill(angles, values, alpha=0.1, color=colors[idx % len(colors)])

    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_title('Comparativo de Descritores', fontsize=13, pad=20)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--inputs', required=True, nargs='+')
    p.add_argument('--labels', required=True, nargs='+')
    p.add_argument('--outdir', default='Atividade3/resultados_q2')
    args = p.parse_args()

    ensure_dir(args.outdir)

    images = []
    labels = []
    descriptors = []
    histograms = []

    for path, label in zip(args.inputs, args.labels):
        img = load_gray(path)
        save_u8(img, os.path.join(args.outdir, f'gray_{label}.png'))
        desc = describe_image(img)
        hist = compute_histogram(img)
        images.append(img)
        labels.append(label)
        descriptors.append(desc)
        histograms.append(hist)
        print(f'\n[{label}]')
        for k, v in desc.items():
            print(f'  {k}: {v}')

    hist_path = os.path.join(args.outdir, 'histogramas_comparativos.png')
    save_histogram_figure(histograms, labels, hist_path)

    comparison_path = os.path.join(args.outdir, 'comparativo_imagens.png')
    save_comparison_figure(images, labels, descriptors, comparison_path)

    radar_path = os.path.join(args.outdir, 'radar_descritores.png')
    save_radar_chart(descriptors, labels, radar_path)

    results = {}
    for label, desc in zip(labels, descriptors):
        results[label] = desc

    json_path = os.path.join(args.outdir, 'resultados_q2.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f'\nResultados salvos em {args.outdir}')


if __name__ == '__main__':
    main()