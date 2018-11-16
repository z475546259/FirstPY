import sys
import os
import dlib
import glob
from skimage import io


current_path = os.getcwd()# 获取当前路径
predictor_path =current_path+"\\shape_predictor_68_face_landmarks.dat"
face_rec_model_path = current_path+"\\dlib_face_recognition_resnet_model_v1.dat"
faces_folder_path = current_path+"\\image"

# Load all the modelswe need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
detector =dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


# Now process all the images
for f in glob.glob(os.path.join(faces_folder_path,"*.jpg")):
    print("Processing file: {}".format(f))
    img = io.imread(f)

    win = dlib.image_window()
    win.clear_overlay()
    win.set_image(img)

    # Ask the detector to find the bounding boxes of eachface. The 1 in the
    # second argument indicates that weshould upsample the image 1 time. This
    # will make everything bigger andallow us to detect more faces.
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    shape2=sp(img,dets[0])
    win.add_overlay(shape2)
    win.add_overlay(dets)

    # Now process each face we found.
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {}Bottom: {}".format(
            k, d.left(), d.top(),d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
        shape = sp(img,d)
        # Draw the face landmarks on the screen so we can seewhat face is currently being processed.
        #win.clear_overlay()
        #win.add_overlay(d)
        win.add_overlay(shape)

        # Compute the 128D vector that describes the face in imgidentified by
        # shape.  In general, if two face descriptor vectorshave a Euclidean
        # distance between them less than0.6 then they are from the same
        # person, otherwise they are fromdifferent people. Here we just print
        # the vector to the screen.
        face_descriptor = facerec.compute_face_descriptor(img,shape)
        print(face_descriptor)

    dlib.hit_enter_to_continue()
