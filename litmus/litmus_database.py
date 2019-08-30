import os
import json
import math
from .color_space import CVC

class Litmus():
    db = []
    cell = {}
    supernova = []
    family = {}

    @classmethod
    def initialize(cls, method):
        if method == "Json":
            with open("static/secret/LitmusGroup 20190801.json") as f:
                cj = json.loads(f.read())
            for index, value in enumerate(cj):
                room = str(value['Cell'])
                cls.cell.update({room: {'list':[], 'group':value['Group'], 'owner':{'star':0} }})

            with open("static/secret/LitmusDB 20190830.json") as f:
                dj = json.loads(f.read())
            
            for index, value in enumerate(dj):
                name = value['Name']
                hexa = value['Hexa']
                rgb = CVC.hexa_rgb(hexa)
                wheel = cls.get_wheel(rgb, 'lab')
                room = cls.get_cell(rgb)
                cell = {'room':room, 'owner':{}} # room 은 cell의 방번호, cell 은 순번
                cls.cell[room]['list'].append(index)
                group = cls.get_group(room, 'cell')
                star = 6 - int(value['Class'][0:1]) 
                if star > cls.cell[room]['owner']['star'] :
                    cls.cell[room]['owner'] = {'id':index, 'name':name, 'star':star}
                category_id = int(value['Category'][0:2]) -1
                category_name = value['Category'][3:]
                family_name = value['Family']
                if family_name not in cls.family.keys() :
                    cls.family.update({ family_name:{'list':[], 'category':{'id':category_id, 'name':category_name}, 'owner':{'star':0} } })
                cls.family[family_name]['list'].append(index)
                if star > cls.family[family_name]['owner']['star'] :
                    cls.family[family_name]['owner'] = {'id':index, 'name':name, 'star':star}
                family = {'name':family_name, 'owner':{}}
                geo = CVC.rgb_GEOlab(rgb, profile='sRGB', illuminant='D65_2')
                text = cls.get_text(wheel)
                
                litmus = {
                    'id': int(index), 
                    'name': name, 
                    'hexa': hexa,
                    'star': star,
                    'family': family,
                    'rgb': rgb, 
                    'geo': geo,
                    'cell': cell,
                    'group': group,
                    'wheel': wheel,
                    'text': text,
                    }
                cls.db.append(litmus)
                if star == 5 :
                    cls.supernova.append({'id': index, 'case':'supernova', 'litmus':litmus})  

        # Set cell owner name after data read and preset
        cls.set_owner()


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
    def set_owner():
        for litmus in Litmus.db :
            litmus_id = litmus['id']
            owner_id = Litmus.cell[litmus['cell']['room']]['owner']['id']
            name = Litmus.db[owner_id]['name']
            hexa = Litmus.db[owner_id]['hexa']
            text = Litmus.db[owner_id]['text']
            Litmus.db[litmus_id]['cell']['owner'].update({'id':owner_id, 'name':name, 'hexa':hexa, 'text':text})
            owner_id = Litmus.family[litmus['family']['name']]['owner']['id'] 
            name = Litmus.db[owner_id]['name']
            hexa = Litmus.db[owner_id]['hexa']
            text = Litmus.db[owner_id]['text']
            Litmus.db[litmus_id]['family']['owner'].update({'id':owner_id, 'name':name, 'hexa':hexa, 'text':text})
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
                H_name = 'Purple-Red'
            elif hue >= 328 :
                H_name = 'Purple'
            elif hue >= 307 :
                H_name = 'Blue-Purple'
            elif hue >= 216 :
                H_name = 'Blue'
            elif hue >= 158 :
                H_name = 'Green-Blue'
            elif hue >= 123 :
                H_name = 'Green'
            elif hue >= 100 :
                H_name = 'Green-Yellow'
            elif hue >= 74 :
                H_name = 'Yellow'
            elif hue >= 41 :
                H_name = 'Yellow-Red'
            elif hue >= 10 :
                H_name = 'Red'
            else :
                H_name = 'Purple-Red'

            L = int(bright*20)
            C = int(chroma/0.15)

            if C >= 5 :
                C_name = "Vivid"
            elif C >= 3 :
                if L >= 14 :
                    C_name = "Light"
                elif L >= 7 :
                    C_name = "Medium"
                else :
                    C_name = "Deep"
            elif C >= 1 :
                if L >= 16 :
                    C_name = "Pale"
                elif L >= 11 :
                    C_name = "Soft"
                elif L >= 6 :
                    C_name = "Dull"
                else :
                    C_name = "Dark"
            else :
                H_name = "Gray"
                if L >= 17 :
                    H_name = 'White'
                    C_name = ''
                elif L >= 13 :
                    C_name = "Light"
                elif L >= 9 :
                    C_name = "Medium"
                elif L >= 4 :
                    C_name = "Dark"
                else :
                    H_name = 'Black'
                    C_name = ''
            wheel = {'H_name':H_name, 'C_name':C_name, 'C': C, 'L': L, }
        return wheel
        
    @staticmethod
    def get_text(wheel) :
        L = wheel['L']
        if L > 10 :
            text_color = '#000000'
            text_font = 'bold'
        else :
            text_color = '#FFFFFF'
            text_font = 'normal'
        return {'color': text_color, 'font': text_font}


    