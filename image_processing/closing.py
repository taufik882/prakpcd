import cv2

def apply_closing(image, kernel):
    result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return result
