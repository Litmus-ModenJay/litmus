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
                wheel = cls.get_wheel(rgb, 'lab')
                depth = cls.get_depth(HSL)
                
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
                    'wheel': wheel,
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
            conv = {'R':'Red', 'O':'Orange', 'Y':'Yellow', 'G':'Green', 'B':'Blue', 'Pr':'Purple', 'P':'Pink', 'Br':'Brown', 
                        'W':'White', 'Gr':'Gray', 'K':'Black'}
            ab = Litmus.cell[room]['group']
            group = conv[ab]
        return group

    @staticmethod
    def get_wheel(rgb, method) :
        if method == 'lab':
            XYZ = CVC.rgb_XYZ(rgb, 'sRGB')
            lab = CVC.XYZ_Labuv(XYZ, 'D65_2')
            bright, chroma, hue = lab[0], lab[5], lab[3]

            if hue >= 350 :
                H_name = 'PR'
            elif hue >= 328 :
                H_name = 'P'
            elif hue >= 307 :
                H_name = 'BP'
            elif hue >= 216 :
                H_name = 'B'
            elif hue >= 158 :
                H_name = 'GB'
            elif hue >= 123 :
                H_name = 'G'
            elif hue >= 100 :
                H_name = 'GY'
            elif hue >= 74 :
                H_name = 'Y'
            elif hue >= 41 :
                H_name = 'YR'
            elif hue >= 10 :
                H_name = 'R'
            else :
                H_name = 'PR'

            L = int(bright*20)
            C = int(chroma/0.15)

            if C >= 5 :
                C_name = "vivid"
            elif C >= 3 :
                if L >= 14 :
                    C_name = "light"
                elif L >= 7 :
                    C_name = "medium"
                else :
                    C_name = "deep"
            elif C >= 1 :
                if L >= 16 :
                    C_name = "pale"
                elif L >= 11 :
                    C_name = "soft"
                elif L >= 6 :
                    C_name = "dull"
                else :
                    C_name = "dark"
            else :
                H_name = "Gy"
                if L >= 17 :
                    H_name = 'Wh'
                    C_name = ''
                elif L >= 13 :
                    C_name = "light"
                elif L >= 9 :
                    C_name = "medium"
                elif L >= 4 :
                    C_name = "dark"
                else :
                    H_name = 'BK'
                    C_name = ''
            wheel = {'H_name':H_name, 'C_name':C_name, 'C': C, 'L': L, }
        return wheel
        
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

    