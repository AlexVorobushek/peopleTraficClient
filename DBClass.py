from datetime import datetime
import sqlite3
import datetime


class DBClass:
    def __init__(self, db_path, camera_name) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cur = self.connection.cursor()

        self.camera_name = camera_name
    
    def new_camera(self, **kwargs):
        import params
        test_at_static_picture = 'true' if params.TEST_AT_STATIC_PICTURE else 'false'

        command = f"""INSERT INTO params VALUES('{kwargs['name']}',
         {kwargs['vertical_viewing_angle']},
         {kwargs['horisontal_viewing_angle']},
         {kwargs['tilt_angle']},
         {kwargs['capture_width']},
         {kwargs['capture_height']},
         {kwargs['port_id']},
         {test_at_static_picture});"""

        self.cur.execute(command)
        self.connection.commit()
    
    def get_camera_params(self) -> dict:
        res = self.cur.execute(f"SELECT * FROM params WHERE name = '{self.camera_name}';").fetchone()
        column_names = [desc[0] for desc in self.cur.description]
        return dict(zip(column_names, res))
    
    def get_all_recordes(self):
        result = self.cur.execute(f"SELECT * FROM {self.camera_name};").fetchall()
        column_names = [desc[0] for desc in self.cur.description]
        return list(map(lambda x: dict(zip(column_names, x)), result))
    
    def close(self):
        self.connection.close()
    
    def search_record_by_datetime(self, datetime:datetime) -> dict:
        camera_recordes = self.get_all_recordes()
        for record in camera_recordes[::-1]:
            if record['datetime'] <= str(datetime):
                return record
        return camera_recordes[0]

    @staticmethod
    def activate(camera_name):
        from params import db_params
        return DBClass(**db_params, camera_name=camera_name)
