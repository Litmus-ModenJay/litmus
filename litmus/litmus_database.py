import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    # group = ['Red', 'Orange', 'Yellow', 'Green', 'cyan', 'Blue', 'Purple', 'Pink', 'Brown', 'White', 'Gray', 'Black']
    depth = ['Light', 'Soft', 'Deep', 'Dark']
    supernova = []
    giant = []
    proxi_origin = []

    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("static/secret/Litmus 20190407.json") as f:
                dj = json.loads(f.read())
            # for index, value in enumerate(dj['Default']):
            for index, value in enumerate(dj):
                name = value['Name']
                hexa = value['Hexa']
                star = value['Class']
                family = value['Family'].split(';')
                if family == '':
                    family = 'Single'
                rgb = CVC.hexa_rgb(hexa)
                litmus = {
                    'id':index, 
                    'name':name, 
                    'hexa':hexa,
                    'star':star,
                    'family':family,
                    'rgb': rgb, 
                    # 'geo': CVC.rgb_GEOrgb(rgb),
                    # 'geo': CVC.rgb_GEOHSL(rgb),
                    # 'geo': CVC.rgb_GEOluv(rgb, profile='CIE RGB', illuminant='D65 2'),
                    'geo': CVC.rgb_GEOlab(rgb, profile='sRGB', illuminant='D65 2'),
                    #'group':'',
                    'group':cls.get_group(rgb, 'rgb'),
                    'depth':cls.get_depth(rgb),
                    'proximity':{}
                    }
                if star == 'Supernova':
                    cls.supernova.append({'id':litmus['id'], 'case':'supernova', 'litmus':litmus})
                if star == 'Giant' or star == 'Supernova':
                    cls.giant.append({'id':litmus['id'], 'case':'giant', 'litmus':litmus})
                cls.db.append(litmus)
            # Calculate Proximity Origin
            cls.proxi_origin = Litmus.get_proxy_origin('rgb supernova')
            
    @staticmethod
    def count():
        return len(Litmus.db)

    @staticmethod
    def get_by_id(id):
        litmus = Litmus.db[id]
        proximity = Litmus.get_proximity(litmus['rgb'], 'rgb')
        litmus.update({'proximity':proximity})
        return litmus

    @staticmethod
    def classify_by_group(sort, order):
        db = {}
        for star in Litmus.supernova:
            db.update({star['litmus']['name']: {'count':0, 'litmus':[] }})
        for litmus in Litmus.db:
            group = litmus['group']
            db[group]['count'] = db[group]['count'] + 1
            db[group]['litmus'].append(litmus)
        keys = db.keys()
        for group in keys:
            if order == "ascend":
                db[group]['litmus'] = sorted(db[group]['litmus'], key=lambda g: g[sort])
            elif order == "descend":
                db[group]['litmus'] = sorted(db[group]['litmus'], reverse=True, key=lambda g: g[sort])
        
        return db
        
    @staticmethod
    def get_proxy_origin(method):
        proxi_origin = []
        if method == 'rgb supernova':
            for supernova in Litmus.supernova:
                name = supernova['litmus']['name']
                hexa = supernova['litmus']['hexa']
                rgb = supernova['litmus']['rgb']
                proxi_origin.append({'name':name, 'rgb':rgb, 'hexa':hexa})

        if method == 'rgb family-center':
            origin = {}
            for supernova in Litmus.supernova:
                origin.update({supernova['litmus']['name']: {'count':0, 'rgb':(0,0,0) }})
            for litmus in Litmus.db:
                if litmus['star'] == 'Planet':
                    for supernova in Litmus.supernova:
                        name = supernova['litmus']['name']
                        for family in litmus['family']:
                            if family == name:
                                count = origin[name]['count']+1
                                rgb = tuple(origin[name]['rgb'][i] + litmus['rgb'][i] for i in range(0,3))
                                origin.update({name: {'count':count, 'rgb':rgb} })
            for supernova in Litmus.supernova:
                name = supernova['litmus']['name']
                hexa = supernova['litmus']['hexa']
                rgb = tuple(origin[name]['rgb'][i] / origin[name]['count'] for i in range(0,3))
                proxi_origin.append({'name':name, 'rgb':rgb, 'hexa':hexa})
        return proxi_origin

    @staticmethod
    def get_proximity(rgb, method):
        if method == 'rgb':
            proximity = []
            for proxi in Litmus.proxi_origin:
                origin = proxi['rgb']
                distance = ((rgb[0]-origin[0])**2 + (rgb[1]-origin[1])**2 + (rgb[2]-origin[2])**2)**0.5
                proximity.append({'name':proxi['name'], 'hexa':proxi['hexa'], 'distance':distance})
            sorted_p = sorted(proximity, key=lambda p: p['distance'])
        return sorted_p

    @staticmethod
    def get_depth(rgb) :
        L = CVC.rgb_HSLrgb(rgb)[2]
        depth = ''
        if L >= 0.75 :
            depth = "Light"
        elif L >= 0.5 :
            depth = "Soft"
        elif L >= 0.25 :
            depth = "Deep"
        else :
            depth = "Dark"
        return depth

    @staticmethod
    def get_group(rgb, method):
        if method == 'rgb':
            HSL = CVC.rgb_HSLrgb(rgb)
            H, L, C = HSL[0], HSL[2], HSL[3]
            group = ''
            if L > 0.9 :
                group = "White"
            elif L < 0.1 :
                group = "Black"
            else :
                if C < 0.1 :
                    group = "Gray"
                else :
                    if H >= 15 and H < 45 :
                        if L >= 0.4 :
                            group = "Orange"
                        else :
                            group = "Brown"
                    elif H >= 45 and H < 75 :
                        group = "Yellow"
                    elif H >= 75 and H < 105 :
                        if L >= 0.5 :
                            if H >= 90 :
                                group = "Green"
                            else :
                                group = "Yellow"
                        else :
                            group = "Green"
                    elif H >= 105 and H < 135 :
                        group = "Green"
                    elif H >= 135 and H < 165 :
                        if L >= 0.5 :
                            group = "Cyan"
                        else :
                            group = "Green"
                    elif H >= 165 and H < 195 :
                        if L < 0.5 :
                            if H >= 180 :
                                group = "Blue"
                            else :
                                group = "Green"
                        else :
                            group = "Cyan"
                    elif H >= 195 and H < 225 :
                        if L >= 0.5 :
                            group = "Cyan"
                        else :
                            group = "Blue"
                    elif H >= 225 and H < 255 :
                        group = "Blue"
                    elif H >= 255 and H < 285 :
                        if L >= 0.5 :
                            group = "Purple"
                        else :
                            group = "Blue"
                    elif H >= 285 and H < 315 :
                        if L < 0.7 :
                            group = "Purple"
                        else :
                            group = "Pink"
                    elif H >= 315 and H < 345 :
                        if L < 0.7 :
                            if H >= 330 :
                                group = "Red"
                            else :
                                group = "Purple"
                        else :
                            group = "Pink"
                    else :
                        if L < 0.7 :
                            group = "Red"
                        else :
                            group = "Pink"
        return group 
