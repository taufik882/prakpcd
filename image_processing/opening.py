import cv2

def apply_opening(image, kernel):
    result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return result
