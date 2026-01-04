import cv2

def apply_dilation(image, kernel, iterations=1):
    result = cv2.dilate(image, kernel, iterations=iterations)
    return result
