
from utils import *

#创建一个detector类，接收从camera传过来的图像，用于检测人脸，识别人脸，并把识别结果返回给Window类

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
import time

class Detector(QObject):

    # 定义一个信号，用于将识别结果传递给Window类

    detect_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.process_this_frame = True
        self.name = "UnKnown"
        self.frame = None
        self.load_data()
        
        
    def load_data(self):
        self.face_encodings = []
        self.face_names = []
        self.face_ids = []
        self.face_info = load_face_info('faces.pkl')
        for key, value in self.face_info.items():
            self.face_encodings.append(value['face_encoding'])
            self.face_names.append(value['name'])
            self.face_ids.append(value['id'])
         
    def Qimage2CvMat(self, image):
        buf = image.bits().asstring(image.byteCount())
        # 将字节流转换为numpy数组
        img = np.frombuffer(buf, dtype=np.uint8).reshape(image.height(), image.width(), 3)
        # 将numpy数组转换为cv2图像
        cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return cv2_img
    
    def detect(self, frame):
        # 如果frame是路径，则读取图像
        self.name = "UnKnown"
        self.id = "UnKnown"
        if isinstance(frame, str):
            resize_frame = read_img(frame)
        else:
            resize_frame = cv2.resize(frame[0], (224, 224))
        face_locations = face_recognition.face_locations(resize_frame)
        face_encodings = face_recognition.face_encodings(
            resize_frame, face_locations)
        for face_encoding in face_encodings:
            # 与已知人脸进行比对
            matches = face_recognition.compare_faces(
                self.face_encodings, face_encoding)
            # 如果是已知人脸，则标记出人名
            if True in matches:
                first_match_index = matches.index(True)
                self.name = self.face_names[first_match_index]
                self.id = self.face_ids[first_match_index]
        self.detect_signal.emit({'name':self.name,'id':self.id}) 
        
        return self.name
        
        



