import cv2

video_path = "DeepfakeExample.mp4"  # Replace 'your_video.mp4' with the actual path to your video file

# Open the video file
cap = cv2.VideoCapture(video_path)

# Set the frame number to capture
frame_to_capture = 565  

# Set a flag to check if the frame is captured
frame_captured = False

while True:
    ret, frame = cap.read()

    if not ret or frame is None or frame.size == 0:
        print("Error reading frame.")
        break

    cv2.imshow("Frame", frame)

    # Capture the specified frame
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == frame_to_capture and not frame_captured:
        cv2.imwrite("captured_frame.jpg", frame)
        print(f"Frame {frame_to_capture} captured and saved as 'captured_frame.jpg'")
        frame_captured = True  # Set the flag to True to avoid capturing the same frame again

    key = cv2.waitKey(30) & 0xFF
    if key == ord("q") or frame_captured:
        break

cap.release()
cv2.destroyAllWindows()
