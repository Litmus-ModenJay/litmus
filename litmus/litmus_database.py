import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    group = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink', 'brown', 'white', 'gray', 'black']
    depth = ['light', 'soft', 'deep', 'dark']
    
    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("static/secret/litmus.json") as f:
                dj = json.loads(f.read())
            for index, value in enumerate(dj['Default']):
                hexa = value['index']
                rgb = CVC.hexa_rgb(hexa)
                cls.db.append({
                    'id':index, 
                    'name':value['name'], 
                    'hexa':hexa,
                    'rgb': rgb,
                    #'geo': CVC.rgb_GEOrgb(rgb),
                    'geo': CVC.rgb_GEOluv(rgb, profile='sRGB', illuminant='D65 2'),
                    'group':CVC.rgb_group(rgb),
                    'depth':CVC.rgb_depth(rgb)
                    })
            return

    @staticmethod
    def count():
        return len(Litmus.db)

    @staticmethod
    def get_by_id(id):
        return Litmus.db[id]

    @staticmethod
    def classify_by_group(sort, order):
        db = {}
        for group in Litmus.group:
            db.update({group: {'count':0, 'data':[] }})
        for litmus in Litmus.db:
            group = litmus['group']
            db[group]['count'] = db[group]['count'] + 1
            db[group]['data'].append(litmus)
        keys = db.keys()
        for group in keys:
            if order == "ascend":
                sorted(db[group]['data'], key=lambda g:  g[sort])
            elif order == "descend":
                sorted(db[group]['data'], reverse=True, key=lambda g:  g[sort])
        
        return db

