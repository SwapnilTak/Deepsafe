import cv2
import dlib
from imutils.video import VideoStream
from collections import deque

EAR_THRESH = 0.2
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
vs = VideoStream(vs = VideoStream(src="DeepfakeExample.mp4"))
vs.start()

blink_count = 0
prev_blink_time = None
NORMAL_BLINK_FREQ = 15
NORMAL_BLINK_DUR = 0.2
blink_durations = deque(maxlen=10)

while True:
    frame = vs.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame)
    for face in faces:
        landmarks = predictor(frame, face)

        left_eye, right_eye = landmarks[36:42], landmarks[42:48]
        left_EAR, right_EAR = _compute_EAR(left_eye), _compute_EAR(right_eye)

        if left_EAR < EAR_THRESH and right_EAR < EAR_THRESH:
            if prev_blink_time is None or time.time() - prev_blink_time > 0.5:
                blink_count += 1
                prev_blink_time = time.time()
                blink_durations.append(time.time() - prev_blink_time)

        _draw_landmarks(frame, landmarks)

    if blink_count > 0:
        blink_freq = 60 * blink_count / (time.time() - vs.startTime)
        avg_blink_dur = sum(blink_durations) / len(blink_durations)

        similarity_score = 0.5 * (abs(NORMAL_BLINK_FREQ - blink_freq) / NORMAL_BLINK_FREQ + abs(NORMAL_BLINK_DUR - avg_blink_dur) / NORMAL_BLINK_DUR)

    cv2.putText(frame, f"Blink Count: {blink_count}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"Similarity Score: {similarity_score:.2f}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Eye Blink Detection", frame)

    if similarity_score < 0.6:
        print("Warning: Potential deepfake detected!")

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

vs.stop()
cv2.destroyAllWindows()

def _compute_EAR(eye):
    A, B, C = eye[0], eye[3], eye[6]
    left_length = cv2.norm(A - B)
    right_length = cv2.norm(C - B)
    ear = (2.0 * cv2.norm(A - C)) / (left_length + right_length)
    return ear

def _draw_landmarks(frame, landmarks):
    for landmark in landmarks:
        cv2.circle(frame, landmark.point, 2, (255, 0, 0), -1)
