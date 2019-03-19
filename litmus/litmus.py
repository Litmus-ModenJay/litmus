import os
import json
import math
from .color import ColorVector

class Litmus():
    db = []
    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("litmus/litmus.json") as f:
                dj = json.loads(f.read())
            for index, value in enumerate(dj['Default']):
                hexa = value['index']
                vector = ColorVector(hexa)
                cls.db.append({
                    'id':index, 
                    'name':value['name'], 
                    'hexa':hexa.upper,
                    'rgb':vector.rgb['norm'],
                    'sphere':vector.rgb['sphere'],
                    'group':vector.group,
                    'depth':vector.depth
                    })
            return

    @staticmethod
    def data():
        return Litmus.db

    @staticmethod
    def count():
        return len(Litmus.db)

