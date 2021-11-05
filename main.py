from MapClass import MapClass
from DBClass import DBClass

from datetime import datetime

visibility_map = MapClass.activate('camera1')
visibility_map.filling_from_db_by_datetime(datetime.now())
visibility_map.draw()
