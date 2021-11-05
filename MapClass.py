from datetime import datetime
from textwrap import fill
from PIL import Image, ImageDraw
import json

from TrigonometryClass import Trigonometry as tr
from DBClass import DBClass



class MapClass:
    def __init__(self, camera_params: dict) -> None:
        self.camera_params = camera_params
        beta = self.camera_params['vertical_viewing_angle']
        alpha = self.camera_params['tilt_angle'] - beta / 2

        self.widht = int((tr.cos(alpha)*camera_params['capture_width'])/tr.cos(alpha+beta))
        self.height = int(((tr.cos(alpha)*tr.tan(alpha+beta)-tr.sin(alpha)) /
                       (2*tr.sin(beta/2)))*camera_params['capture_height'])
        self.peoples = []

    def projectPointOntoMap(self, point: tuple) -> tuple:
        beta = self.camera_params['vertical_viewing_angle']
        alpha = self.camera_params['tilt_angle'] - beta / 2
        captureHeight = self.camera_params['capture_height']
        captureWidth = self.camera_params['capture_width']

        pointY = point[1]
        pointX = point[0]

        newPointY = pointY * (tr.cos(alpha)*tr.tan(alpha+beta) - tr.sin(alpha))/(2*tr.sin(beta/2))
        newPointX = (pointY/captureHeight)*(self.widht-captureWidth)/2 + \
         (((captureHeight-pointY)/captureHeight)*(tr.cos(alpha)/tr.cos(alpha+beta)-1)+1)*pointX

        coors = int(newPointX), int(newPointY)
        return coors
    
    def draw(self):
        camera_capture_width = self.camera_params['capture_width']
        camera_capture_heigth = self.camera_params['capture_height']

        img = Image.new("RGB", (self.widht, self.height), (50, 50, 50))
        d = ImageDraw.Draw(img,)
        d.polygon(((0, 0), (self.widht, 0), self.projectPointOntoMap((camera_capture_width, camera_capture_heigth)), self.projectPointOntoMap((0, camera_capture_heigth))), fill=(100, 100, 100))

        for x, y in self.peoples:
            # d.point((x, y), (255, 255, 255))
            d.ellipse((x-3, y-3, x+3, y+3), (255, 255, 255))
        
        img.save('images/map.jpg')
    
    def __str__(self) -> str:
        return json.dumps(self.peoples)
    
    def add_point_at_map(self, point):
        self.peoples.append(point)

    def filling_from_db_by_datetime(self, datetime:datetime):
        db = DBClass.activate(self.camera_params['name'])
        record = db.search_record_by_datetime(datetime)
        db.close

        self.peoples = json.loads(record['map'])

    @staticmethod
    def activate(camera_name):
        camera_params = DBClass.activate(camera_name).get_camera_params()
        return MapClass(camera_params)
