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
        self.coordinates = '37.620070,55.753630'
        self.scale = 10
        self.size = '650,450'  # ограничение по размеру: 650х450
        self.map_file = "map.png"
        self.pixmap = QPixmap()
        self.get_image()
        self.set_image()

    def get_image(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.coordinates}&l=map&" \
                      f"apikey=40d1649f-0493-4b70-98ba-98533de7710b&size={self.size}&z={str(self.scale)}"
        response = requests.get(map_request)
        with open(self.map_file, "wb") as f:
            f.write(response.content)
        print(response)

    def set_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.scale >= 1:
                self.scale -= 1
        if event.key() == Qt.Key_PageUp:
            if self.scale < 17:
                self.scale += 1
        self.get_image()
        self.set_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec_())
