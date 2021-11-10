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


#  main window class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pages/untitled.ui', self)
        self.button_create_camera.clicked.connect(open_create_camera_window)
        self.button_delete_camera.clicked.connect(self.clicked_delete_camera)
        self.button_update_camera_records.clicked.connect(self.clicked_update_camera_records)
        self.list_camera_records.itemClicked.connect(self.camera_record_cliced)
    
    def update_cameras_list(self):
        all_cameras_names = get_camera_list_by_db()

        self.comboBox_camera_name.clear()
        self.comboBox_camera_name.addItems(
            all_cameras_names
        )
    
    def clicked_delete_camera(self):
        CameraController.delete_camera(
            self.comboBox_camera_name.currentText()
        )
        self.update_cameras_list()
    
    def clicked_update_camera_records(self):
        db = DBClass.activate(
            self.comboBox_camera_name.currentText()
        )
        records_amount = int(self.spin_show_last.text())
        camera_records = db.get_all_recordes(['id', 'datetime'])
        if len(camera_records) > records_amount:
            camera_records = camera_records[:records_amount]
        camera_records = ['\t'.join(map(str, record.values())) for record in camera_records]

        self.list_camera_records.clear()
        self.list_camera_records.addItems(
            camera_records
        )
    
    def camera_record_cliced(self, line_text):
        line_text = line_text.text()

        self.map_name.setText(
            self.comboBox_camera_name.currentText()+' '+line_text.split("\t")[-1]
        )
        record_id = int(line_text.split()[0])
        visibility_map = MapClass.activate(
            self.comboBox_camera_name.currentText()
        )
        visibility_map.filling_from_db_by_id(
            record_id
        )
        img = visibility_map.draw()
        # self.image.pixmap(img)
        # код код код код код
        # код код код код код
        # код код код код код
        # код код код код код   Нада обновить изображение
        # код код код код код
        # код код код код код
        # код код код код код


#  create camera window class
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
        main_window.update_cameras_list()
        self.close()


def activate():
    app = QApplication(sys.argv)
    global main_window
    main_window = Window()
    main_window.update_cameras_list()
    main_window.show()
    sys.exit(app.exec_())
