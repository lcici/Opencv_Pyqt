import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog,QApplication, QFileDialog
from PyQt5.uic import loadUi
import cv2


class Life2Coding(QDialog):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def __init__(self):
        super(Life2Coding,self).__init__()
        loadUi("firstui.ui",self)

        self.image = None
        self.processImage = None
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        self.detectButton.clicked.connect(self.detectClicked)
       # self.hSlider.valueChanged.connect(self.cannyDisplay)
        


    @pyqtSlot()
    def loadClicked(self):
        fname, filter= QFileDialog().getOpenFileName(self, "Open File", "C:\\Users\c386liu\PycharmProjects\ODmeter", "Image Files(*.jpg)")
        if fname:
            self.loadImage("picture1.jpg")
        else:
            print("Invalid image")

    @pyqtSlot()
    def saveClicked(self):
        fname, filter = QFileDialog.getSaveFileName(self, "Save File", "C:\\Users\c386liu\PycharmProjects\ODmeter", "Image Files(*.jpg)")
        if fname:
            cv2.imwrite(fname, self.processImage)
        else:
            print("Error")

    @pyqtSlot()
    def detectClicked(self):
        gray= cv2.cvtColor(self.processImage, cv2.COLOR_BGR2GRAY) if len(self.image.shape)>=3 else self.image
        faces=self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            if self.chkFace.isChecked():
                cv2.rectangle(self.processImage, (x, y), (x+w, y+h), (255,0, 0), 2)
            else:
                self.processImage = self.image.copy()
            roi_gray= gray[y:y+h, x:x+w]
            roi_color= self.processImage[y:y+h, x:x+w]
            if self.chkEye.isChecked():
                eyes= self.eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew, ey+eh), (0,255,0), 2)
            else:
                self.processImage[y:y+h, x:x+w] = self.image[y:y+h, x:x+w].copy()
        self.displayImage(2)

    @pyqtSlot()
    def cannyDisplay(self):
        gray= cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(self.image.shape)>=3 else self.image
        self.processImage=cv2.Canny(gray, self.hSlider.value(), self.hSlider.value()*3)
        self.displayImage(2)


    def loadImage(self, fname):
        self.image = cv2.imread(fname)
        self.processImage = self.image.copy()
        self.displayImage(1)

    def displayImage(self, window = 1):
        qformat=QImage.Format_Indexed8
        if len(self.processImage.shape) == 3: #rows[0], col[1], channels[2]
            if(self.processImage.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        img=QImage(self.processImage, self.processImage.shape[1], self.processImage.shape[0],
                   self.processImage.strides[0], qformat)
        img = img.rgbSwapped()
        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(img))
            self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        if window == 2:
            self.processLabel.setPixmap(QPixmap.fromImage(img))
            self.processLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


app=QApplication(sys.argv)
window = Life2Coding()
window.setWindowTitle("First UI")
window.setGeometry(200,200, 600, 600)
window.show()
sys.exit(app.exec_())
