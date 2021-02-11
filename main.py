import sys
import requests

from design import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.coordinates = ''
        self.scale = ''
        self.map_file = "map.png"
        self.get_coordinates()
        self.get_scale()
        self.get_image()

    def get_coordinates(self):
        self.coordinates = self.lineEdit.text()

    def get_scale(self):
        self.scale = self.lineEdit_2.text()

    def get_image(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.coordinates}&l=map&apikey=40d1649f-0493-4b70-98ba" \
                      f"-98533de7710b&z={self.scale}"
        response = requests.get(map_request)
        with open(self.map_file, "wb") as f:
            f.write(response.content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec_())
