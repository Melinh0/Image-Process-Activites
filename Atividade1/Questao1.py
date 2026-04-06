import numpy as np
from PIL import Image

def rgb_to_grayscale(img_array):
    """Conversão manual de RGB para escala de cinza."""
    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
    return (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)

def gaussian_kernel(size, sigma=1):
    """Cria um kernel Gaussiano 2D normalizado."""
    kernel = np.fromfunction(
        lambda x, y: (1/(2*np.pi*sigma**2)) * np.exp(-((x-(size-1)/2)**2 + (y-(size-1)/2)**2) / (2*sigma**2)),
        (size, size)
    )
    return kernel / np.sum(kernel)

def convolve(img, kernel):
    """Aplica convolução manual com padding."""
    k_size = kernel.shape[0]
    pad = k_size // 2
    img_pad = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = img_pad[i:i+k_size, j:j+k_size]
            output[i,j] = np.sum(region * kernel)
    return output

def pencil_sketch(image_path, output_path, kernel_size=21, sigma=5):
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    gray = rgb_to_grayscale(img_array)
    kernel = gaussian_kernel(kernel_size, sigma)
    blurred = convolve(gray, kernel)
    epsilon = 1e-8
    sketch = (gray.astype(np.float32) / (blurred.astype(np.float32) + epsilon)) * 255
    sketch = np.clip(sketch, 0, 255).astype(np.uint8)
    Image.fromarray(sketch).save(output_path)
    return gray, blurred, sketch