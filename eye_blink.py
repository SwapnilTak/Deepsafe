import cv2
import dlib

def detect_faces_eyes(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Initialize the face detector and shape predictor from dlib
    face_detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor(dlib.data.get_file("shape_predictor_68_face_landmarks.dat"))

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_detector(gray_image)

    # Initialize Dlib's face and eye detector
    predictor_path = dlib.data.get_file("shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    # Draw blue rectangles around the faces and eyes
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Use Dlib's shape predictor to find facial landmarks (including eyes)
        landmarks = predictor(gray_image, face)
        for n in range(36, 48):  # Region of interest for eyes in the 68-point landmarks
            x_eye, y_eye = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(image, (x_eye, y_eye), 2, (255, 0, 0), -1)

    # Save the resulting image
    output_path = "output_image_dlib.jpg"
    cv2.imwrite(output_path, image)
    print(f"Face and eye boundaries saved to {output_path}")

if __name__ == "__main__":
    # Specify the path to the input image
    input_image_path = "captured_image.jpg"

    # Call the function to detect faces and eyes, draw boundaries, and save the result
    detect_faces_eyes(input_image_path)
