import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from CameraController import CameraController
from DBClass import DBClass
from params import db_params
from MapClass import MapClass


def open_create_camera_window():
    global create_camera_window
    create_camera_window = CCWindow()
    create_camera_window.show()

def get_camera_list_by_db() -> list:
    connection = sqlite3.connect(db_params['db_path'])
    cursor = connection.cursor()
    result = [i[0] for i in cursor.execute(f"SELECT name FROM params;").fetchall()]
    return result


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pages/untitled.ui', self)
        self.button_create_camera.clicked.connect(open_create_camera_window)
        self.button_delete_camera.clicked.connect(self.clicked_delete_camera)
        self.button_update_camera_records.clicked.connect(self.clicked_update_camera_records)
        # код код код код код
        # код код код код код
        # код код код код код
        # код код код код код   Нада подключить функцию self.open_map при клике на элемент в списке
        # код код код код код
        # код код код код код
        # код код код код код
    
    def update_cameras_list(self):
        all_cameras_names = get_camera_list_by_db()
        # код код код код код
        # код код код код код
        # код код код код код
        # код код код код код   Нада обновить элементы в выпадающем списке
        # код код код код код
        # код код код код код
        # код код код код код
    
    def clicked_delete_camera(self):
        CameraController.delete_camera(
            self.comboBox_camera_name.text()
        )
        self.update_cameras_list()
    
    def clicked_update_camera_records(self):
        db = DBClass.activate(
            self.comboBox_camera_name.text()
        )
        records_amount = self.spin_show_last.text()
        camera_records = db.get_all_recordes(['id', 'datatime'])
        if len(camera_records) > records_amount:
            camera_records = camera_records[:records_amount]
        camera_records = ['\t'.join(i) for i in camera_records]
        # код код код код код
        # код код код код код
        # код код код код код
        # код код код код код   Нада обновить элементы в списке
        # код код код код код
        # код код код код код
        # код код код код код
    
    def open_map(self, record_id: int):
        visibility_map = MapClass.activate(
            self.comboBox_camera_name.text()
        )
        visibility_map.filling_from_db_by_id(
            record_id
        )
        img = visibility_map.draw()
        # код код код код код
        # код код код код код
        # код код код код код
        # код код код код код   Нада обновить изображение
        # код код код код код
        # код код код код код
        # код код код код код


class CCWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('pages/create_camera_page.ui', self)
        self.cancel_btn.clicked.connect(self.close)
        self.create_btn.clicked.connect(self.clicked_create_button)
    
    def clicked_create_button(self):
        CameraController.create_camera(
            name = self.name_line.text(),
            vertical_viewing_angle = self.vva_spin.text(),
            horisontal_viewing_angle = self.hva_spin.text(),
            tilt_angle = self.ta_spin.text(),
            capture_width = self.cw_spin.text(),
            capture_height = self.ch_spin.text(),
            port_id = self.port_id_spin.text(),
        )
        first_window.update_cameras_list()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    first_window = Window()
    first_window.show()
    sys.exit(app.exec_())
