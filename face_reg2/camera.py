#实现一个camera类来控制摄像头，并使用pyqt5的多线程来实现摄像头的实时显示
# camera类的功能是打开摄像头，关闭摄像头，获取摄像头的图像，获取摄像头的状态
# 通过多线程来实现摄像头的实时显示

from PyQt5.QtCore import QThread, pyqtSignal
import cv2
from PyQt5.QtGui import QImage, QPixmap
from detect import Detector
from PIL import Image, ImageDraw, ImageFont, ImageQt
class Camera(QThread):
    change_pixmap_signal = pyqtSignal(dict)
    send_pixmap_signal = pyqtSignal(list)
    def __init__(self):
        super(Camera, self).__init__()
        self._run_flag = True
        self._cap = None
        self._frame = None
        self._camera_status = False
        self.i=0
        self.detector = Detector()
        self.thread = QThread(self)
        self.send_pixmap_signal.connect(self.detector.detect)
        self.detector.detect_signal.connect(self.draw_name)
        self.detector.moveToThread(self.thread)
        
        self.font =  ImageFont.truetype('simsun.ttc', 40)
        self.fillColor = (0,0,255)
        self.position = (10,30)
        self.draw = None
    def run(self):
        
        while self._run_flag:
            ret, self._frame = self._cap.read()
            if ret:
                self.i += 1
                rgb_frame = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB)
                
                if self.i%5==0:
                    self._frame = rgb_frame
                    self.send_pixmap_signal.emit([rgb_frame])
                cv2.waitKey(30)
    
    def open_camera(self, camera_id):
        if not self._camera_status:
            try:    
                self._cap = cv2.VideoCapture(camera_id)
                self._camera_status = True
                self.detector.load_data()
                self.thread.start()
            except:
                print('打开摄像头失败')
                self._camera_status = False

    def close_camera(self):
        if self._camera_status:
            self._run_flag = False
            self._cap.release()
            self._camera_status = False
            self.thread.quit()
            self.thread.wait()

    def get_frame(self):
        return self._frame

    def get_camera_status(self):
        return self._camera_status
    
    def draw_name(self, info):
        name = info['name']
        img_PIL = Image.fromarray(self._frame)
        draw = ImageDraw.Draw(img_PIL)
        draw.text(self.position,name,font=self.font, fill=self.fillColor)
        pixmap = ImageQt.ImageQt(img_PIL)
        self.change_pixmap_signal.emit({'image':pixmap, 'info':info})