import params
import sqlite3


class CameraController():
    @staticmethod
    def create_new_params_record(cursor, connection, **camera_params):
        test_at_static_picture = 'true' if params.TEST_AT_STATIC_PICTURE else 'false'
        command = f"""INSERT INTO params VALUES('{camera_params['name']}',
         {camera_params['vertical_viewing_angle']},
         {camera_params['horisontal_viewing_angle']},
         {camera_params['tilt_angle']},
         {camera_params['capture_width']},
         {camera_params['capture_height']},
         {camera_params['port_id']},
         {test_at_static_picture});"""

        cursor.execute(command)
        connection.commit()
    
    @staticmethod
    def create_new_camera_table(cursor, connection, camera_name):
        command = f'''
        CREATE TABLE {camera_name} (
            id       INTEGER  PRIMARY KEY AUTOINCREMENT,
            datetime DATETIME,
            map      STRING
        );
        '''
        cursor.execute(command)

    @staticmethod
    def create_camera(**camera_params):
        connection = sqlite3.connect(
            params.db_params['db_path']
        )
        cursor = connection.cursor()
        CameraController.create_new_params_record(cursor, connection, **camera_params)
        CameraController.create_new_camera_table(cursor, connection, camera_params['name'])

        connection.close()
    
    @staticmethod
    def delete_camera(camera_name):
        connection = sqlite3.connect(
            params.db_params['db_path']
        )
        cursor = connection.cursor()

        #  delete camera table
        command = f"DROP TABLE {camera_name};"
        cursor.execute(command)

        #  delete camera params
        command = f'DELETE FROM params WHERE name = "{camera_name}";'
        cursor.execute(command)

        connection.commit()
        connection.close()
