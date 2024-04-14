import face_recognition
import cv2
import numpy as np
import pickle
import os

def get_face_encoding(img):
    '''
        从图片中获取人脸编码
    '''
    face_locations = face_recognition.face_locations(img)
    if len(face_locations) == 0:
        return None
    face_encoding = face_recognition.face_encodings(img, face_locations)[0]
    return face_encoding

def read_img(filename):
    img = cv2.imdecode(np.fromfile(filename,dtype=np.uint8), 1) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resize_img = cv2.resize(img, (224, 224))
    return resize_img
        
 
