import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    cell = []
    # group = ['Red', 'Orange', 'Yellow', 'Green', 'cyan', 'Blue', 'Purple', 'Pink', 'Brown', 'White', 'Gray', 'Black']
    group = []
    depth = ['Light', 'Soft', 'Deep', 'Dark']
    supernova = []
    giant = []
    proxi_origin = []

    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("static/secret/LitmusGroup 20190801.json") as f:
                cj = json.loads(f.read())
            for index, value in enumerate(cj):
                cell = {'id':index, 'room':value['Cell'], 'color':value['Group']}
                cls.cell.append(cell)

            with open("static/secret/LitmusDB 20190815.json") as f:
                dj = json.loads(f.read())
            # for index, value in enumerate(dj['Default']):
            for index, value in enumerate(dj):
                name = value['Name']
                hexa = value['Hexa']
                star = value['Class']
                family = value['Family']
                category = value['Category']
                keyword = value['Keyword']
                rgb = CVC.hexa_rgb(hexa)
                litmus = {
                    'id':index, 
                    'name':name, 
                    'hexa':hexa,
                    'star':star,
                    'family':family,
                    'category':category,
                    'keyword':keyword,
                    'rgb': rgb, 
                    # 'geo': CVC.rgb_GEOrgb(rgb),
                    # 'geo': CVC.rgb_GEOHSL(rgb),
                    # 'geo': CVC.rgb_GEOluv(rgb, profile='sRGB', illuminant='D65_2'),
                    'geo': CVC.rgb_GEOlab(rgb, profile='sRGB', illuminant='D65_2'),
                    #'group':'',
                    'cell':cls.get_cell(rgb),
                    'group':cls.get_group(rgb, 'cell'),
                    'depth':cls.get_depth(rgb),
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
    def get_cell(rgb):
        room_r = int((rgb[0]*64)//8 + 1)
        if room_r >= 9:
            room_r = 8
        room_g = int((rgb[1]*64)//8 + 1)
        if room_g >= 9:
            room_g = 8
        room_b = int((rgb[2]*64)//8 + 1)
        if room_b >= 9:
            room_b = 8  
        room = str(room_r) + str(room_g) + str(room_b)
        return room

    @staticmethod
    def get_group(rgb, method):
        if method == 'cell':
            room_r = (rgb[0]*64)//8
            if room_r >= 8:
                room_r = 7
            room_g = (rgb[1]*64)//8
            if room_g >= 8:
                room_g = 7
            room_b = (rgb[2]*64)//8
            if room_b >= 8:
                room_b = 7  
            room = int(room_r*64 + room_g*8 + room_b)
            group = Litmus.cell[room]['color']
        return group

    @staticmethod
    def get_group_old(rgb, method):
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
