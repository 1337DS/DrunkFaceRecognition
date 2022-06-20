import cv2
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier("haarcascade_eye.xml")
import mediapipe as mp
import numpy as np
import imutils
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
from PIL import Image

import re
import dlib
import cv2
import os


def allign_face(img_path):
    # load the dlib or cv2 face detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
    
    img = cv2.imread(img_path)
    # determine eyes and nose coordinates
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    #print(rects)
    #cv2.imshow('Face', img)
    # Terminate the process
    #cv2.waitKey(0)
    #cv2.destroyWindow('Face')
    #cv2.waitKey(1)
    
    if len(rects) > 0:
        for rect in rects:
            x = rect.left()
            y = rect.top()
            w = rect.right()
            h = rect.bottom()
            shape = predictor(gray, rect)

    shape = shape_to_normal(shape)
    nose, left_eye, right_eye = get_eyes_nose_dlib(shape)
    
    # find center of the line between two eyes 
    center_of_forehead = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)
    
    # find the center of its top side
    center_pred = (int((x + w) / 2), int((y + y) / 2))

    length_line1 = distance(center_of_forehead, nose)
    length_line2 = distance(center_pred, nose)
    length_line3 = distance(center_pred, center_of_forehead)
    
    # retrieve the angle in radians
    cos_a = cosine_formula(length_line1, length_line2, length_line3)
    angle = np.arccos(cos_a)
    
    
    rotated_point = rotate_point(nose, center_of_forehead, angle)
    rotated_point = (int(rotated_point[0]), int(rotated_point[1]))
    if is_between(nose, center_of_forehead, center_pred, rotated_point):
        angle = np.degrees(-angle)
    else:
        angle = np.degrees(angle)
    
    img = rotate_image(img, angle)
    
    #cv2.imshow('Face', img)
    # Terminate the process
    #cv2.waitKey(0)
    #cv2.destroyWindow('Face')
    #cv2.waitKey(1)
    return img
    
def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)    

def shape_to_normal(shape):
    shape_normal = []
    for i in range(0, 5):
        shape_normal.append((i, (shape.part(i).x, shape.part(i).y)))
    return shape_normal

def get_eyes_nose_dlib(shape):
    nose = shape[4][1]
    left_eye_x = int(shape[3][1][0] + shape[2][1][0]) // 2
    left_eye_y = int(shape[3][1][1] + shape[2][1][1]) // 2
    right_eyes_x = int(shape[1][1][0] + shape[0][1][0]) // 2
    right_eyes_y = int(shape[1][1][1] + shape[0][1][1]) // 2
    return nose, (left_eye_x, left_eye_y), (right_eyes_x, right_eyes_y)

def cosine_formula(length_line1, length_line2, length_line3):
    cos_a = -(length_line3 ** 2 - length_line2 ** 2 - length_line1 ** 2) / (2 * length_line2 * length_line1)
    return cos_a

def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy

def is_between(point1, point2, point3, extra_point):
    c1 = (point2[0] - point1[0]) * (extra_point[1] - point1[1]) - (point2[1] - point1[1]) * (extra_point[0] - point1[0])
    c2 = (point3[0] - point2[0]) * (extra_point[1] - point2[1]) - (point3[1] - point2[1]) * (extra_point[0] - point2[0])
    c3 = (point1[0] - point3[0]) * (extra_point[1] - point3[1]) - (point1[1] - point3[1]) * (extra_point[0] - point3[0])
    if (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0):
        return True
    else:
        return False

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def check_for_face(img_path):
    # Load the face detector
    detector = dlib.get_frontal_face_detector()
    # Read the input image
    img = cv2.imread(img_path)
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray', gray)
    # Terminate the process
    #cv2.waitKey(0)
    #cv2.destroyWindow('Gray')
    #cv2.waitKey(1)
    # Detect faces
    detector = dlib.get_frontal_face_detector()
    face = detector(gray, 0)
    #print(type(face))
    if len(face) != 0:
        face_detected = True
    else:
        face_detected = False
    #cv2.imshow('Face', img)
    # Terminate the process
    #cv2.waitKey(0)
    #cv2.destroyWindow('Face')
    #cv2.waitKey(1)
    return face_detected

def allign_all_faces_in_directory(abs_path_input_dir, abs_path_ouput_dir):
    
    # check if dir exists
    if not os.path.exists(abs_path_ouput_dir):
        os.mkdir(abs_path_ouput_dir)
    
    input_files = [os.path.join(dp,f) for dp, dn, fn in os.walk(os.path.expanduser(abs_path_input_dir)) for f in fn]
    for input_file in input_files:
        #print(input_file)
        if check_for_face(input_file) == True:
            file_name = input_file.split('/')[-1]
            print(file_name)
            
            path_to_safe = abs_path_ouput_dir + '/' + file_name
            img = allign_face(input_file)
            cv2.imwrite(path_to_safe, img)
    
abs_path_input_dir = '/Users/yannikhubrich/Documents/Studium/6Semester/DrunkFaceRecognition/Data/raw/cropped_to_four'
abs_path_ouput_dir = '/Users/yannikhubrich/Documents/Studium/6Semester/DrunkFaceRecognition/Data/raw/alligned'

allign_all_faces_in_directory(abs_path_input_dir, abs_path_ouput_dir)