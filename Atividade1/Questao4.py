import numpy as np
from PIL import Image

def negative(img_array):
    return 255 - img_array

def rescale_intensity(img_array, new_min=100, new_max=200):
    old_min, old_max = 0, 255
    img_float = img_array.astype(np.float32)
    rescaled = ((img_float - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return rescaled  

def reverse_even_rows(img_array):
    output = img_array.copy()
    for i in range(0, output.shape[0], 2):
        output[i] = output[i, ::-1]
    return output

def mirror_top_to_bottom(img_array):
    h = img_array.shape[0]
    half = h // 2
    output = img_array.copy()
    output[half:] = output[:half][::-1]
    return output

def vertical_flip(img_array):
    return img_array[::-1, :]

def apply_all_transformations(image_path, output_path):
    img = Image.open(image_path).convert('L')
    arr = np.array(img, dtype=np.float32) 
    arr = negative(arr)
    arr = rescale_intensity(arr)
    arr = reverse_even_rows(arr)
    arr = mirror_top_to_bottom(arr)
    arr = vertical_flip(arr)  
    arr = np.clip(arr, 0, 255).astype(np.uint8) 
    Image.fromarray(arr).save(output_path)
    return arr