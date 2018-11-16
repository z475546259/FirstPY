#!/usr/bin/env python
# -*- coding: utf-8 -*-
import face_recognition
import cv2
import numpy as np
import glob
import os
import logging
IMAGES_PATH = './images' # put your reference images in here
CAMERA_DEVICE_ID = 0
MAX_DISTANCE = 0.6 # increase to make recognition less strict, decrease to make more strict


def get_face_embeddings_from_image(image, convert_to_rgb=False):
    """Take a raw image and run both the face detection and face embedding model on it
    """
    # Convert from BGR to RGB if needed
    if convert_to_rgb:
        image = image[:, :, ::-1]
    # run the face detection model to find face locations
    face_locations = face_recognition.face_locations(image)
    # run the embedding model to get face embeddings for the supplied locations
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_locations, face_encodings



def setup_database():
    """
        Load reference images and create a database of their face encodings
    """
    database = {}
    for filename in glob.glob(os.path.join(IMAGES_PATH, '*.jpg')):
        # load image
        image_rgb = face_recognition.load_image_file(filename)
        # use the name in the filename as the identity key
        identity = os.path.splitext(os.path.basename(filename))[0]
        # get the face encoding and link it to the identity
        locations, encodings = get_face_embeddings_from_image(image_rgb)
        database[identity] = encodings[0]
    return database



# open a connection to the camera
video_capture = cv2.VideoCapture(CAMERA_DEVICE_ID)
# read from the camera in a loop, frame by frame
while video_capture.isOpened():
    # Grab a single frame of video
    ok, frame = video_capture.read()

    #
    # do face recognition stuff here using this frame...
    #
    # Display the image
    cv2.imshow('my_window_name', frame)
    # Hit 'q' on the keyboard to stop the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # release handle to the webcam
    video_capture.release()
    # close the window (buggy on a Mac btw)
    cv2.destroyAllWindows()



def paint_detected_face_on_image(frame, location, name=None):
    """
        Paint a rectangle around the face and write the name
    """
    # unpack the coordinates from the location tuple
    top, right, bottom, left = location
    if name is None:
        name = '未知'
        color = (0, 0, 255) # red for unrecognized face
    else:
        tts("欢迎回家，张治强~")
        color = (0, 128, 0) # dark green for recognized face
    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 20), (right, bottom), color, cv2.FILLED)

    from PIL import Image, ImageDraw, ImageFont

    cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)

    # PIL图片上打印汉字
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
    draw.text((left+6, bottom-18 ), name, (255, 255, 255), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

    # PIL图片转cv2 图片
    img_OpenCV = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    frame = img_OpenCV
    return frame
    # cv2.imshow("print chinese to image", img_OpenCV)
    # cv2.waitKey(3000)






    # cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)


























def run_face_recognition(database):
    """
    Start the face recognition via the webcam
    """
    # Open a handler for the camera
    video_capture = cv2.VideoCapture(CAMERA_DEVICE_ID)
    # the face_recognitino library uses keys and values of your database separately
    known_face_encodings = list(database.values())
    known_face_names = list(database.keys())
    while video_capture.isOpened():
        # Grab a single frame of video (and check if it went ok)
        ok, frame = video_capture.read()
        if not ok:
            logging.error("Could not read frame from camera. Stopping video capture.")
            break
        # run detection and embedding models
        face_locations, face_encodings = get_face_embeddings_from_image(frame, convert_to_rgb=True)
        # Loop through each face in this frame of video and see if there's a match
        for location, face_encoding in zip(face_locations, face_encodings):
            # get the distances from this encoding to those of all reference images
            distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            # select the closest match (smallest distance) if it's below the threshold value
            if np.any(distances <= MAX_DISTANCE):
                best_match_idx = np.argmin(distances)
                name = known_face_names[best_match_idx]
            else:
                name = None
            # put recognition info on the image
            frame = paint_detected_face_on_image(frame, location, name)
            # Display the resulting image
            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



def tts(txt):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(txt)
    engine.runAndWait()


database = setup_database()
run_face_recognition(database)
