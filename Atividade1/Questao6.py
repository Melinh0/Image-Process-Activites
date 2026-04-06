import numpy as np
from PIL import Image

def quantize(image_path, output_path, levels):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=np.float32)
    step = 256 / levels
    quantized = np.floor(img_array / step) * step
    quantized = np.clip(quantized, 0, 255).astype(np.uint8)
    Image.fromarray(quantized).save(output_path)
    return quantized