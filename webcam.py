import cv2
import numpy as np

def detect_colors():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges in HSV
        color_ranges = {
            'blue': (np.array([100, 50, 50]), np.array([130, 255, 255])),
            'cyan': (np.array([80, 50, 50]), np.array([100, 255, 255])),
            'red1': (np.array([0, 50, 50]), np.array([10, 255, 255])),
            'red2': (np.array([170, 50, 50]), np.array([180, 255, 255])),
            'orange': (np.array([10, 50, 50]), np.array([25, 255, 255]))
        }

        # Dictionary to store contours for each color
        color_contours = {}

        # Process each color
        for color, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            color_contours[color] = contours

        # Combine red masks
        mask_red = cv2.bitwise_or(
            cv2.inRange(hsv, color_ranges['red1'][0], color_ranges['red1'][1]),
            cv2.inRange(hsv, color_ranges['red2'][0], color_ranges['red2'][1])
        )
        red_contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color_contours['red'] = red_contours

        # Draw rectangles around detected areas
        for color, contours in color_contours.items():
            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    if color == 'blue':
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    elif color == 'cyan':
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    elif color == 'red':
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    elif color == 'orange':
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)

        # Display the result
        cv2.imshow('Color Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Run the function
detect_colors()
