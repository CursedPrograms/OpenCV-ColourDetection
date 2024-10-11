import cv2
import numpy as np

def detect_colors(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define color ranges in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    lower_cyan = np.array([80, 50, 50])
    upper_cyan = np.array([100, 255, 255])
    
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    
    lower_orange = np.array([10, 50, 50])
    upper_orange = np.array([25, 255, 255])
    
    # Create masks for each color
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_cyan = cv2.inRange(hsv, lower_cyan, upper_cyan)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    
    # Apply masks to the original image
    result_blue = cv2.bitwise_and(image, image, mask=mask_blue)
    result_cyan = cv2.bitwise_and(image, image, mask=mask_cyan)
    result_red = cv2.bitwise_and(image, image, mask=mask_red)
    result_orange = cv2.bitwise_and(image, image, mask=mask_orange)
    
    # Combine results
    result = cv2.add(result_blue, result_cyan)
    result = cv2.add(result, result_red)
    result = cv2.add(result, result_orange)
    
    # Display results
    cv2.imshow('Original Image', image)
    cv2.imshow('Detected Colors', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Usage
detect_colors('path_to_your_image.jpg')
