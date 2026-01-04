import cv2

def load_image(path, mode="rgb"):
    if mode == "gray":
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(path, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Gagal membaca citra dari path yang diberikan")

    return image
