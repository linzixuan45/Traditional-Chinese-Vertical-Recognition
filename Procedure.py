import sys, os
import cv2
import numpy as np
from PyQt5.QtWidgets import *
# from main_ui import *
from UI import *
from OCR import *
import datetime
import pandas as pd
import time


Brose_path = []
save_path = "img_temp"


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.__init()
        self.project = BaiduOcr(self.API_KEY, self.SECRET_KEY)  # 创建一个实例对象
        self.temp_path = save_path  # 新创建的txt文件的存放路径
        self.setupUi(self)
        self.pushButton.clicked.connect(self.show_img)  # 打开图片
        self.pushButton_2.clicked.connect(self.align_image)  # 文档自动矫正和优化
        self.pushButton_3.clicked.connect(self.hand_align_image)  # 图片手动矫正
        self.pushButton_4.clicked.connect(self.bin_image)  # 灰度化二值化
        self.pushButton_5.clicked.connect(self.convert_simple)  # 繁体转简体
        self.pushButton_8.clicked.connect(self.save_image)  # 结果保存
        self.pushButton_9.clicked.connect(self.detect_image)  # 单图篡改检测
        self.pushButton_10.clicked.connect(self.detectmore_image)  # 多图篡改检测


    def hand_align_image(self):
        pass

    def convert_simple(self):
        pass
    def bin_image(self):
        pass

    def align_image(self):
        pass

    # show image
    def show_img(self):
        global pic_path
        pic_path, _ = QFileDialog.getOpenFileName(self, '显示图片', '/Users/', 'Image files(*.jpg *.gif *.png *.tif)')

        if pic_path:
            self.text_create(pic_path)
            self.qt_print_path(pic_path)
            print(pic_path)
            image2 = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            print(image2.shape)
            show = cv2.resize(image2, (300, 300))
            show2 = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 数据变成QImage形式
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示的Label里 显示QImage

    def __init(self):
        self.date = str(datetime.date.today())
        s = json.load(open("setting.json", "r", encoding="utf-8"))
        self.API_KEY = s['API_KEY']
        self.SECRET_KEY = s['SECRET_KEY']
        self.imgs_dir = s['imgs_dir']
        self.acc_loc = s['acc_loc']
        self.word_save_dir = s['word_save']
        self.img_temp_dir = s['img_temp']
        self.dpi = s['dpi']
        if s['path_sort_way'] == 'string':
            self.sort_way = 1

        elif s['path_sort_way'] == 'int':
            self.sort_way = 2
        else:
            print("sort_Way must be string or int ")
            sys.exit()

    # detect

    def detect_image(self):
        global pic_path
        pic_path, _ = QFileDialog.getOpenFileName(self, '显示图片', '/Users/', 'Image files(*.jpg *.gif *.png *.tif)')
        QMessageBox.information(self, "检测中", "检测中，请稍等！", QMessageBox.Yes | QMessageBox.No)
        if pic_path:
            self.qt_print_path(pic_path)
            image2 = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            show = cv2.resize(image2, (300, 300))
            show2 = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 数据变成QImage形式
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示的Label里 显示QImage

        task_name = os.path.basename(pic_path).split('.')[0]
        acc_poem, img_save_path, json_dict_1 = self.project.inference(pic_path, self.img_temp_dir, acc_loc=self.acc_loc, dpi=self.dpi)
        self.qt_print("\n")
        self.qt_print(f"{acc_poem}")
        pic_path = img_save_path

        if pic_path:
            self.qt_print_path(pic_path)
            image2 = cv2.imdecode(np.fromfile(pic_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            show = cv2.resize(image2, (300, 300))
            show2 = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 数据变成QImage形式
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示的Label里 显示QImage

    def detectmore_image(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹",
                                                     "./")
        self.text_create(directory)
        QMessageBox.information(self, "检测中", "检测中，请稍等！先喝杯茶吧。", QMessageBox.Yes | QMessageBox.No)

        task_name = os.path.basename(directory) + self.date
        inference_dir(self.project, directory, self.word_save_dir, self.img_temp_dir, task_name=task_name, acc_loc=self.acc_loc, dpi=self.dpi,
                      sort_way=self.sort_way)
        QMessageBox.information(self, "完成了！", "恭喜你！完成啦！", QMessageBox.Yes | QMessageBox.No)

    def text_create(self, msg):
        full_path = os.path.join(self.temp_path, 'fileaddress.txt')  # 也可以创建一个.doc的word文档
        file = open(full_path, 'w')
        file.write(msg)



    # save
    def save_image(self):
        result = os.path.exists(os.path.join(self.temp_path, 'fileaddress.txt'))
        if result == True:
            pic_path = os.path.join(self.temp_path, 'pic_temp.png')
            self.text_create(os.path.join(self.temp_path, "rectangle_result.png"))
            QMessageBox.information(self, "成功了！", "图像已保存！", QMessageBox.Yes | QMessageBox.No)
            image2 = cv2.imread(pic_path)
            show = cv2.resize(image2, (800, 600))
            show2 = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        else:
            QMessageBox.information(self, "错误", "请选择一张图片！", QMessageBox.Yes | QMessageBox.No)

    def qt_print(self, message):
        self.textBrowser.insertPlainText(message)

    def qt_print_path(self, path):
        self.textBrowser.insertPlainText(pic_path)
        Brose_path.append(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
