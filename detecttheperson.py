
import cv2
import pygame
import numpy as np
from tensorflow import keras
from plyer import notification
import weeklyupdate
# Load the pre-trained model
model = keras.models.load_model('Model/nail_biting_model10.h5')

# Create a VideoCapture object to capture the video from webcam
cap = cv2.VideoCapture(0)

# Load the face detection cascade classifier
net=cv2.dnn.readNetFromCaffe('Model/deploy.prototxt', 'Model/res10_300x300_ssd_iter_140000.caffemodel')
# Define the input size of the model
INPUT_SIZE = (150, 150)

# Define a function to preprocess the image before passing it to the model
def preprocess_image(img):
    img = cv2.resize(img, INPUT_SIZE)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img

# Define a function to perform nail-biting detection on the input frame
def detect_nail_biting(frame, biting_counter):

    # Resize the frame to a fixed width and height for face detection
    resized_frame = cv2.resize(frame, (150, 150))
    cv2.putText(frame, 'To stop, press q', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    # Create a blob from the resized frame
    blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Set the blob as input to the face detection model
    net.setInput(blob)

    # Perform face detection
    detections = net.forward()

    # check if any face is detected
    if not detections.shape[2]:
        cv2.putText(frame,'No face detected', (10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    else:
        # Loop over all the detected faces
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections
            if confidence > 0.5:
                # Get the coordinates of the bounding box
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype(int)

                # Extract the face region
                face = frame[startY:endY, startX:endX]

                # Preprocess the face image
                face = preprocess_image(face)

                # Make a prediction using the model
                pred = model.predict(face)

                # Get the predicted class label
                label = 'Biting' if pred[0][0] > 0.5 else 'Not biting'
                prob = pred[0][0] if label == 'Biting' else 1 - pred[0][0]
                if label == 'Biting':
                    biting_counter += 1
                    color = (0, 0, 255)
                    print(biting_counter)

                else:
                    color = (0, 255, 0)
                    biting_counter = 0

                # Draw a rectangle around the face and display the label
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                cv2.putText(frame, f'{label} ({prob:.2f})', (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Display the resulting frame
        cv2.imshow('Nail Biting Detection', frame)

        return biting_counter


def run_nail_biting_detection(name):
    biting_counter = 0
    audio_path = "Model/Alexa Simple Alarm Sound (320 kbps).mp3"
    pygame.mixer.init()

    # Main loop to capture and process frames from the webcam
    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()
        # Check if the frame was successfully captured
        if not ret:
            break

        # Call the detect_nail_biting function to perform detection on the frame
        biting_counter = detect_nail_biting(frame, biting_counter)

        if biting_counter > 8:
            weeklyupdate.date_for_weekly(1,name)
            notification.notify("Nail Biting Detected", "Stop biting your nail!", app_name="", timeout=2, ticker='', toast=False, app_icon="icons/icon2.ico")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            pygame.time.wait(2400)
            pygame.mixer.music.stop()
            biting_counter = 0

        if cv2.waitKey(1)==ord('q'):

            break
    cap.release
    cv2.destroyWindow("Nail Biting Detection")

