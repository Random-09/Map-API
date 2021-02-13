import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
# from design import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):  # Ui_MainWindow
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        # self.setupUi(self)
        self.api_key = '40d1649f-0493-4b70-98ba-98533de7710b'
        self.w = 37.620070
        self.h = 55.753630
        self.scale = 0
        self.spn_W, self.spn_H = 90, 45
        self.size = '650,450'  # ограничение по размеру: 650х450
        self.cur_map = 'map'
        self.map_file = "map.png"
        self.pixmap = QPixmap()
        self.get_image()
        self.set_image()

        self.scheme_but.clicked.connect(self.set_scheme)
        self.sat_but.clicked.connect(self.set_sat)
        self.hybrid_but.clicked.connect(self.set_hybrid)

    def get_image(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.w},{self.h}&l={self.cur_map}&" \
                      f"apikey={self.api_key}&size={self.size}&spn={str(self.spn_W)},{str(self.spn_H)}"
        response = requests.get(map_request)
        with open(self.map_file, "wb") as f:
            f.write(response.content)

    def set_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)

    def update_scale(self):
        self.spn_W = 90 / round(2 ** self.scale, 6)
        self.spn_H = 45 / round(2 ** self.scale, 6)
        # print(self.scale)
        # print(self.spn_W, self.spn_H)

    def set_scheme(self):
        self.cur_map = 'map'
        self.map_file = 'map.png'
        self.get_image()
        self.set_image()

    def set_sat(self):
        self.cur_map = 'sat'
        self.map_file = 'map.jpg'
        self.get_image()
        self.set_image()

    def set_hybrid(self):
        self.cur_map = 'sat,skl'
        self.map_file = 'map.png'
        self.get_image()
        self.set_image()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.scale >= 1:
                self.scale -= 1
        if event.key() == Qt.Key_PageUp:
            if self.scale <= 17:
                self.scale += 1
        if event.key() == Qt.Key_Up:
            if self.h + (45 / round(2 ** self.scale, 6)) * 2 < 83:
                self.h += (45 / round(2 ** self.scale, 6)) * 2
        if event.key() == Qt.Key_Down:
            if self.h - (45 / round(2 ** self.scale, 6)) * 2 > -90:
                self.h -= (45 / round(2 ** self.scale, 6)) * 2
        if event.key() == Qt.Key_Right:
            if self.w + (90 / round(2 ** self.scale, 6)) * 2.5 < 180:
                self.w += (90 / round(2 ** self.scale, 6)) * 2.5
        if event.key() == Qt.Key_Left:
            if self.w - (90 / round(2 ** self.scale, 6)) * 2.5 > - 180:
                self.w -= (90 / round(2 ** self.scale, 6)) * 2.5  # цифры работают только на долготе Москвы
        self.update_scale()
        self.get_image()
        self.set_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec_())
