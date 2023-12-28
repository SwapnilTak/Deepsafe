import cv2
import dlib
import os
from concurrent.futures import ThreadPoolExecutor

def detect_faces_eyes(image, detector):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_image)
    
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Use Dlib's shape predictor to find facial landmarks (including eyes)
        landmarks = shape_predictor(gray_image, face)
        for n in range(36, 48):  # Region of interest for eyes in the 68-point landmarks
            x_eye, y_eye = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x_eye, y_eye), 2, (255, 0, 0), -1)

    return image

def process_frame(frame, detector):
    # Detect faces and eyes, and save the outlined frame
    outlined_frame = detect_faces_eyes(frame, detector)
    return outlined_frame

def capture_frames_and_outline(video_path, output_folder, downsampling_factor=2):
    cap = cv2.VideoCapture(video_path)
    detector = dlib.get_frontal_face_detector()

    frame_number = 0
    futures = []

    with ThreadPoolExecutor() as executor:
        while True:
            ret, frame = cap.read()

            if not ret or frame is None or frame.size == 0:
                print("Error reading frame.")
                break

            # Downsampling
            frame = cv2.resize(frame, (frame.shape[1] // downsampling_factor, frame.shape[0] // downsampling_factor))

            # Submit frame processing task to the executor
            futures.append(executor.submit(process_frame, frame.copy(), detector))

            frame_number += 1

    cap.release()

    # Retrieve processed frames from futures
    outlined_frames = [future.result() for future in futures]

    # Save the outlined frames in the output folder
    for i, outlined_frame in enumerate(outlined_frames):
        output_path = os.path.join(output_folder, f"frame_{i}.jpg")
        cv2.imwrite(output_path, outlined_frame)
        print(f"Frame {i} saved: {output_path}")

if __name__ == "__main__":
    video_path = "DeepfakeExample.mp4"
    output_folder = "outlined_frames"
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    capture_frames_and_outline(video_path, output_folder, downsampling_factor=2)

    print(f"All outlined frames saved in '{output_folder}'.")
