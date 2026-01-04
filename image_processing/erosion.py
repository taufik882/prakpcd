import cv2

def apply_erosion(image, kernel, iterations=1):
    result = cv2.erode(image, kernel, iterations=iterations)
    return result
