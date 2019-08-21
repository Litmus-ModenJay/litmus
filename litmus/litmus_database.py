import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    cell = {}
    # group = ['Red', 'Orange', 'Yellow', 'Green', 'Cyan', 'Blue', 'Purple', 'Pink', 'Brown', 'White', 'Gray', 'Black']
    group = []
    depth = ['Light', 'Soft', 'Deep', 'Dark']
    supernova = []
    giant = []
    dwarf = []
    comet = []
    star = {'Supernova':[], 'Giant':[], 'Dwarf':[], 'Comet':[]}
    family = {}
    keyword = { "A.Universe & Star":[], "B. Earth & Nature":[], "C. Plant & Flower":[], "D. Animal & Bird":[], 
                "E. Human Body & Spirit":[], "F. Time & Season":[], "G. Space & Place":[], "H. Wear& Fashion":[], 
                "I. Food & Drink":[], "J. House & Tool":[], "K. Literature & History":[], "M. Art & Color":[], 
                "N. Material & Pigment":[], "O. Science & Technology":[], "P. Military & Society":[] }
    proxi_origin = []

    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("static/secret/LitmusGroup 20190801.json") as f:
                cj = json.loads(f.read())
            for index, value in enumerate(cj):
                room = str(value['Cell'])
                cls.cell.update({room: {'group':value['Group'], 'owner':{'star':''} }})

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
                HSL = CVC.rgb_HSLrgb(rgb)
                geo = CVC.rgb_GEOlab(rgb, profile='sRGB', illuminant='D65_2')
                room = cls.get_cell(rgb)
                cell = {'room':room, 'name':''} # room 은 cell의 방번호, cell 은 순번
                group = cls.get_group(room, 'cell')
                depth = cls.get_depth(HSL)

                # if star not in cls.star.keys() :
                #     cls.star.update({star:[]})
                # cls.star[star].append({'id':index, 'name':name})
                
                if star in cls.star.keys() :
                    cls.star[star].append({'id':index, 'name':name})
                    ownerclass = cls.cell[room]['owner']['star']
                    if star == 'Supernova':
                        cls.cell[room]['owner'] = {'id':index, 'name':name, 'star':star}
                    elif star == 'Giant':
                        if not ownerclass == 'Supernova':
                            cls.cell[room]['owner'] = {'id':index, 'name':name, 'star':star}
                    elif star == 'Dwarf':
                        if ownerclass not in ['Supernova', 'Giant']:
                            cls.cell[room]['owner'] = {'id':index, 'name':name, 'star':star}
                    else :
                        if ownerclass not in ['Supernova', 'Giant', 'Dwarf']:
                            cls.cell[room]['owner'] = {'id':index, 'name':name, 'star':star}

                if family not in cls.family.keys() :
                    cls.family.update({family:[]})
                cls.family[family].append({'id':index, 'name':name})
                
                if keyword not in cls.keyword.keys() :
                    cls.keyword.update({keyword:[]})
                cls.keyword[keyword].append({'id':index, 'name':name, 'category':category})

                litmus = {
                    'id': index, 
                    'name': name, 
                    'hexa': hexa,
                    'star': star,
                    'family': family,
                    'category': category,
                    'keyword': keyword,
                    'rgb': rgb, 
                    'geo': geo,
                    'cell': cell,
                    'group': group,
                    'depth': depth,
                    }
                cls.db.append(litmus)  

        # Set cell owner name after data read and preset
        cls.set_ownername()


    @staticmethod
    def count():
        return len(Litmus.db)

    @staticmethod
    def get_by_id(id):
        litmus = Litmus.db[id]
        # owner = Litmus.cell[litmus['cell']['room']]['owner']['name']
        # litmus.update({'owner':owner})
        return litmus

    @staticmethod
    def set_ownername():
        for litmus in Litmus.db :
            Litmus.db[litmus['id']]['cell']['name'] = Litmus.cell[litmus['cell']['room']]['owner']['name']       
        return

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
    def get_group(room, method):
        if method == 'cell':
            group = Litmus.cell[room]['group']
        return group

    @staticmethod
    def get_depth(HSL) :
        L = HSL[2]
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

    