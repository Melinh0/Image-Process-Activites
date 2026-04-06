import numpy as np
from PIL import Image

def create_mosaic(image_path, output_path, block_size):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    h, w = img_array.shape
    block_h, block_w = h // block_size, w // block_size
    blocks = []
    for i in range(block_size):
        for j in range(block_size):
            block = img_array[i*block_h:(i+1)*block_h, j*block_w:(j+1)*block_w]
            blocks.append(block)
    # Mapeamento da nova ordem (exemplo de permutação)
    new_order = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    mosaic = np.zeros_like(img_array)
    for idx, new_idx in enumerate(new_order):
        i, j = divmod(idx, block_size)
        mosaic[i*block_h:(i+1)*block_h, j*block_w:(j+1)*block_w] = blocks[new_idx]
    Image.fromarray(mosaic).save(output_path)
    return mosaic