import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    group = ['Red', 'Orange', 'Yellow', 'Green', 'cyan', 'Blue', 'Purple', 'Pink', 'Brown', 'White', 'Gray', 'Black']
    depth = ['Light', 'Soft', 'Deep', 'Dark']
    supernovas = []

    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("static/secret/Litmus 20190403.json") as f:
                dj = json.loads(f.read())
            # for index, value in enumerate(dj['Default']):
            for index, value in enumerate(dj):
                name = value['Name']
                hexa = value['Hexa']
                rgb = CVC.hexa_rgb(hexa)
                litmus = {
                    'id':index, 
                    'name':name, 
                    'hexa':hexa,
                    'rgb': rgb, 
                    # 'geo': CVC.rgb_GEOrgb(rgb),
                    # 'geo': CVC.rgb_GEOHSL(rgb),
                    # 'geo': CVC.rgb_GEOluv(rgb, profile='CIE RGB', illuminant='D65 2'),
                    'geo': CVC.rgb_GEOlab(rgb, profile='CIE RGB', illuminant='D65 2'),
                    'group':CVC.rgb_group(rgb),
                    'depth':CVC.rgb_depth(rgb)
                    }
                for star in CVC.supernova():
                    if name == star[0]:
                        cls.supernovas.append({'id':index, 'case':'supernovas', 'litmus':litmus})
                cls.db.append(litmus)
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
        for star in CVC.supernova():
            db.update({star[0]: {'count':0, 'data':[] }})
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

