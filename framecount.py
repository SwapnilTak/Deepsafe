import cv2

# Replace 'your_video.mp4' with the path to your video file
video_path = 'your_video.mp4'

# Open the video file
cap = cv2.VideoCapture("DeepfakeExample.mp4")

# Check if the video file is opened successfully
if not cap.isOpened():
    print(f"Error: Couldn't open video file '{video_path}'")
    exit()

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Release the video capture object
cap.release()

# Print the total number of frames
print(f"Total Frames in '{video_path}': {total_frames}")
