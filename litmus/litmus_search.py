from .litmus_database import Litmus
from .color_space import CVC

def search_main(word):
    search = {}
    if len(word) > 2: # 2글자 이하는 검색에서 제외
        symbol = word[0]
        tag = word[1:]
        if symbol == '#':
            if is_hexa(tag): # 헥사코드인지 확인 - #시작 16진 7 숫자 (#FFFFFF) or 16진 6 숫자 (FFFFFF)
                search = search_by_hexa(word, radius=0.1)
        elif symbol == '&':
            if tag in Litmus.family.keys():
                search = search_by_family(tag)
        elif symbol == '/':
            cap = tag.capitalize()
            if cap in Litmus.keyword.keys():
                search = search_by_keyword(cap)
        elif symbol == '$':
            if tag in Litmus.cell.keys():
                search = search_by_cell(tag)
        elif symbol == '@':
            geo = is_geo(tag)
            if geo :
                search = search_by_geo(geo, radius = 10)
        else:
            search = search_by_name(word)
        if search:
            search.update({'supernova':{'count':len(Litmus.supernova), 'list':Litmus.supernova}})
    return search

def search_info(my_id):
    litmus = Litmus.db[my_id]
    hexa = litmus['hexa']
    family = litmus['family']['name']
    cell = litmus['cell']['room']
    search = search_by_hexa(hexa, radius=0.1)
    for item in search['identical']['list']:
        if my_id == item['id']:
            item['case'] = 'self'
    search.update(search_by_family(family))
    search.update(search_by_cell(cell))
    search.update({'supernova':{'count':len(Litmus.supernova), 'list':Litmus.supernova}})
    return search

def search_by_hexa(hexa, radius):
    me = CVC.hexa_rgb(hexa)
    identical = []
    neighbor = []
    for litmus in Litmus.db:
        you = litmus['rgb']
        d = tuple(abs(you[i] - me[i]) for i in range(0,3))
        if d[0] < radius and d[1] < radius and d[2] < radius: 
            distance = (d[0]**2 + d[1]**2+ d[2]**2)**0.5
            if distance < 0.0001 :
                identical.append({'id': litmus['id'], 'case':'identical', 'distance':distance,'litmus':litmus})
            elif distance < radius:
                neighbor.append({'id': litmus['id'], 'case':'neighbor', 'distance':distance,'litmus':litmus})
    if identical or neighbor:
        sorted_i = sorted(identical, key=lambda i: i['litmus']['name'])
        sorted_n = sorted(neighbor, key=lambda n: n['distance'])
        return {'identical':{'count':len(sorted_i), 'list':sorted_i}, 'neighbor':{'count':len(sorted_n), 'list':sorted_n}}
    else:
        return {}

def search_by_name(word):
    match = []
    for litmus in Litmus.db:
        name = litmus['name']
        if (word.lower() in name.lower()):
            match.append({'id': litmus['id'], 'case':'match', 'litmus':litmus})
    if match:
        sorted_m = sorted(match, key=lambda m: m['litmus']['name'])
        return {'match':{'count':len(sorted_m), 'list':sorted_m}}
    else:
        return {}

def search_by_family(tag): 
    family = []
    for index in Litmus.family[tag]['list']:
        litmus = Litmus.db[int(index)]
        family.append({'id': litmus['id'], 'case':'family', 'litmus':litmus})
    if family:
        sorted_f = sorted(family, key=lambda f: f['litmus']['name'])
        return {'family':{'count':len(sorted_f), 'list':sorted_f}}
    else:
        return {}

def search_by_cell(tag): 
    cell = []
    for index in Litmus.cell[tag]['list']:
        litmus = Litmus.db[int(index)]
        cell.append({'id': litmus['id'], 'case':'cell', 'litmus':litmus})
    if cell:
        sorted_c = sorted(cell, key=lambda c: c['litmus']['name'])
        return {'cell':{'count':len(sorted_c), 'list':sorted_c}}
    else:
        return {}
  
def search_by_geo(geo, radius):
    identical = []
    neighbor = []
    for litmus in Litmus.db:
        you = litmus['geo']
        d = tuple(abs(you[i] - geo[i]) for i in range(0,2))
        if d[0] < radius and d[1] < radius: 
            distance = (d[0]**2 + d[1]**2)**0.5
            if distance < 0.1 :
                identical.append({'id': litmus['id'], 'case':'identical', 'distance':distance,'litmus':litmus})
            elif distance < radius:
                neighbor.append({'id': litmus['id'], 'case':'neighbor', 'distance':distance,'litmus':litmus})
    if identical or neighbor:
        sorted_i = sorted(identical, key=lambda i: i['litmus']['name'])
        sorted_n = sorted(neighbor, key=lambda n: n['distance'])
        return {'identical':{'count':len(sorted_i), 'list':sorted_i}, 'neighbor':{'count':len(sorted_n), 'list':sorted_n}}
    else:
        return {}

def is_hexa(tag):
    if len(tag) == 6:
        hexa = tag
    else :
        return False
    try:
        int(hexa, 16)
        return '#'+ hexa
    except ValueError:
        return False

def is_geo(word):
    if len(word.split(',')) == 2:
        geo = word.split(',')
    else :
        return False
    try:
        for data in geo:
            float(data)
        lat = float(geo[0])
        lng = float(geo[1])
        if lat > 90.0 or lat < -90.0 or lng > 180.0 or lng <= -180.0:
            return False
        return (lat, lng)
    except ValueError:
        return False


