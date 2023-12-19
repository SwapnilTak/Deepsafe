import cv2
import numpy as np

def calculate_brightness(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    brightness = np.mean(gray_frame)
    
    return brightness

def detect_improper_lighting(video_path, threshold=100):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        brightness = calculate_brightness(frame)

        if brightness < threshold:
            cv2.putText(frame, "Improper Lighting", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Lighting Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

video_path = 'path/to/your/video.mp4'

brightness_threshold = 100

detect_improper_lighting(video_path, threshold=brightness_threshold)
