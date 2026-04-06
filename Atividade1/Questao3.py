import numpy as np
from PIL import Image

def weighted_blend(img1_path, img2_path, output_path, alpha=0.5):
    img1 = Image.open(img1_path).convert('L')
    img2 = Image.open(img2_path).convert('L')
    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
        print(f"Aviso: imagem2 redimensionada de {img2.size} para {img1.size}")
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)
    blended = (alpha * arr1 + (1 - alpha) * arr2).astype(np.uint8)
    Image.fromarray(blended).save(output_path)
    return blended