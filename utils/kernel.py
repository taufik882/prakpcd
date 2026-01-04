import numpy as np

def create_kernel(size):
    if size < 1:
        raise ValueError("Ukuran kernel harus lebih besar dari 0")

    if size % 2 == 0:
        size += 1

    kernel = np.ones((size, size), dtype=np.uint8)
    return kernel
