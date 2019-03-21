import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("litmus/litmus.json") as f:
                dj = json.loads(f.read())
            for index, value in enumerate(dj['Default']):
                hexa = value['index']
                rgb = CVC.hexa_rgb(hexa)
                cls.db.append({
                    'id':index, 
                    'name':value['name'], 
                    'hexa':hexa,
                    'rgb': rgb,
                    'geo': CVC.rgb_GEOrgb(rgb),
                    'group':CVC.rgb_group(rgb).capitalize,
                    'depth':CVC.rgb_depth(rgb).capitalize
                    })
            return

    @staticmethod
    def data():
        return Litmus.db

    @staticmethod
    def count():
        return len(Litmus.db)

    @staticmethod
    def get_by_id(id):
        return Litmus.db[id]
