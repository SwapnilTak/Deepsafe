import cv2
from facenet_pytorch import MTCNN
import os

def detect_eyes(image, mtcnn):
    boxes, _ = mtcnn.detect(image)

    if boxes is not None:
        for box in boxes:
            x, y, w, h = map(int, box)
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return image

def process_frame(frame, mtcnn):
    # Detect eyes and save the outlined frame
    outlined_frame = detect_eyes(frame, mtcnn)
    return outlined_frame

def capture_frames_and_outline(video_path, output_folder, downsampling_factor=2, skip_frames=5):
    cap = cv2.VideoCapture(video_path)
    mtcnn = MTCNN(keep_all=True)

    frame_number = 0
    futures = []

    while True:
        # Skip frames
        for _ in range(skip_frames):
            ret, _ = cap.read()
            if not ret:
                break

        ret, frame = cap.read()

        if not ret or frame is None or frame.size == 0:
            print("Error reading frame.")
            break

        # Downsampling
        frame = cv2.resize(frame, (frame.shape[1] // downsampling_factor, frame.shape[0] // downsampling_factor))

        # Submit frame processing task to the executor
        outlined_frame = process_frame(frame.copy(), mtcnn)

        # Save the outlined frame in the output folder
        output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
        cv2.imwrite(output_path, outlined_frame)

        print(f"Frame {frame_number} saved: {output_path}")

        frame_number += 1

    cap.release()

if __name__ == "__main__":
    video_path = "DeepfakeExample.mp4"
    output_folder = "outlined_eyes"

    capture_frames_and_outline(video_path, output_folder, downsampling_factor=2, skip_frames=1)

    print(f"All outlined eye frames saved in '{output_folder}'.")
 