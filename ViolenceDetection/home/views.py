from django.shortcuts import render,redirect
import tensorflow
from tensorflow import keras
from keras import models
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
from ViolenceDetection import settings
import base64
from django.http import HttpResponse
import uuid
from django.conf import settings
from home.models import ViolenceImage

# Load the pre-trained model
MoBiLSTM_model = load_model(r"E:\Study stuff\College\8th Sem 2024\CAPSTONE\Project\Project\CapstoneProject\Files\Another Model\model.keras")
# Constants
CLASSES_LIST = ["NonViolence", "Violence"]
SEQUENCE_LENGTH = 16  
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64

def base(request):
    return render(request,'base.html')

def index(request):
    return render(request,'index.html')
 
def upload(request):
    if request.method == 'POST':
        # Get the uploaded video file from the request
        video_file = request.FILES.get('videoFile')

        # Check if a video file was provided
        if video_file:
            # Save the video file to a temporary location
            video_path = os.path.join(settings.MEDIA_ROOT, 'temp_video.mp4')
            with open(video_path, 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Process the video and check for violence
            result_images = process_video(video_path)

            # Render the template with the result
            return render(request, 'result.html', {'result': result_images})

    # Render the upload form initially
    return render(request, 'upload.html')

def process_video(video_path):
    # Use OpenCV to capture frames from the video
    video_capture = cv2.VideoCapture(video_path)

    # Initialize variables
    frames_list = []
    violence_frames = []
    result_images = []

    ViolenceImage.objects.all().delete()

    # Process each frame in the video
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Preprocess the frame
        resized_frame = cv2.resize(frame, (64, 64))
        normalized_frame = resized_frame / 255.0
        frames_list.append(normalized_frame)

        # Keep the list size within the sequence length
        if len(frames_list) > SEQUENCE_LENGTH:
            frames_list.pop(0)

        # Check if enough frames have been captured
        if len(frames_list) == SEQUENCE_LENGTH:
            # Make prediction
            predicted_labels_probabilities = MoBiLSTM_model.predict(np.expand_dims(frames_list, axis=0))[0]
            predicted_label = np.argmax(predicted_labels_probabilities)
            predicted_class_name = CLASSES_LIST[predicted_label]

            if predicted_class_name == "Violence":
                violence_frames.append(frame)

    # Save up to 5 violence frames as image files in the media folder
    for i, frame in enumerate(violence_frames[:3]):
        # Save the frame as an image file in the media folder
        image_filename = f"violence_frame_{uuid.uuid4()}.jpg"
        image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
        cv2.imwrite(image_path, frame)

        # Create a new ViolenceImage instance and save it to the database
        violence_image = ViolenceImage.objects.create(
            image=image_filename,
            confidence=predicted_labels_probabilities[predicted_label]
        )

        # Append the ViolenceImage instance to the result_images list
        result_images.append(violence_image)

    # Release the video capture object
    video_capture.release()

    return result_images











def realtime(request):
    flag = True
    flag = predict_webcam(SEQUENCE_LENGTH,flag)
    if flag:
        return redirect("/")
    else:
        return render(request,'realtime.html')

    
    


def predict_webcam(SEQUENCE_LENGTH,flag):
    # Open a connection to the webcam (typically 0 for built-in webcam)
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        print("Webcam not detected. Make sure it is connected.")
        return False

    frames_list = []

    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Webcam', cv2.WND_PROP_TOPMOST, 1)  # Set the window to be always on top

    while True:
        # Capture frame from the webcam
        ret, frame = webcam.read()

        # Preprocess the frame
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255.0
        frames_list.append(normalized_frame)

        # Keep the list size within the sequence length
        if len(frames_list) > SEQUENCE_LENGTH:
            frames_list.pop(0)

        # Check if enough frames have been captured
        if len(frames_list) == SEQUENCE_LENGTH:
            # Make prediction
            predicted_labels_probabilities = MoBiLSTM_model.predict(np.expand_dims(frames_list, axis=0))[0]
            predicted_label = np.argmax(predicted_labels_probabilities)
            predicted_class_name = CLASSES_LIST[predicted_label]

            # Display the prediction on the frame
            if predicted_class_name == "Violence":
                cv2.putText(frame, f"Predicted: {predicted_class_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                cv2.putText(frame, f"Predicted: {predicted_class_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            

        # Display the frame
        cv2.imshow('Webcam', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    webcam.release()
    cv2.destroyAllWindows()
    return True