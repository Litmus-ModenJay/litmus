import os
import json
import math
from .colorspace import CVC

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
                # vector = ColorVector(hexa)
                cls.db.append({
                    'id':index, 
                    'name':value['name'], 
                    'hexa':hexa.upper,
                    'rgb': rgb,
                    'geo': CVC.rgb_GEOrgb(rgb),
                    #'group':vector.group,
                    #'depth':vector.depth
                    })
            return

    @staticmethod
    def data():
        return Litmus.db

    @staticmethod
    def count():
        return len(Litmus.db)

