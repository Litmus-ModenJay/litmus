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
        elif symbol == '/':
            if tag in Litmus.family.keys():
                search = search_by_family(tag)
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
    search.update(get_thesaurus(my_id))
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

def get_thesaurus(litmus_id) :
    thesaurus = {}
    litmus = Litmus.db[litmus_id]
    rgb = litmus['rgb']
    room = litmus['cell']['room']
    r, g, b = room[0:1], room[1:2], room[2:3]
    level = int( (int(r) + int(g) + int(b)) / 2 )
    
    complementary = []
    additive = (1-rgb[0], 1-rgb[1], 1-rgb[2])
    new_id = find_nearest(additive, 0.1)
    new_litmus = Litmus.db[new_id]
    complementary.append({'id': new_id, 'case':'complementary', 'litmus':new_litmus })
    CMYK = CVC.rgb_CMYK(rgb)
    subtractive = ( CMYK[0]*(1-CMYK[3]), CMYK[1]*(1-CMYK[3]), CMYK[2]*(1-CMYK[3]) )
    new_id = find_nearest(subtractive, 0.1)
    new_litmus = Litmus.db[new_id]
    complementary.append({'id': new_id, 'case':'complementary', 'litmus':new_litmus })
    thesaurus.update({'complementary':{'count':len(complementary), 'list':complementary}})

    shade = []
    if level > 2 :
        for i in range (1, level-1) :
            new_rgb = ( rgb[0]*i/level, rgb[1]*i/level, rgb[2]*i/level )
            new_id = find_nearest(new_rgb, 0.1)
            new_litmus = Litmus.db[new_id]
            shade.append({'id': new_id, 'case':'shade', 'litmus':new_litmus })
    if shade :
        thesaurus.update({'shade':{'count':len(shade), 'list':shade}})

    tint = []
    if level < 7 :
        for i in range (1, 12 - level) :
            new_rgb = ( 1-(1-rgb[0])*i/(12-level), 1-(1-rgb[1])*i/(12-level), 1-(1-rgb[2])*i/(12-level) )
            new_id = find_nearest(new_rgb, 0.1)
            new_litmus = Litmus.db[int(new_id)]
            tint.append({'id': new_id, 'case':'tint', 'litmus':new_litmus })
    if tint :
        thesaurus.update({'tint':{'count':len(tint), 'list':tint}})

    adjacent = []
    if int(r) > 1 :
        cell = str(int(r)-1) + g + b
        new_id = Litmus.cell[cell]['owner']['id']
        new_litmus = Litmus.db[new_id]
        adjacent.append({'id': new_id, 'case':'adjavent', 'litmus':new_litmus })
    if int(r) < 8 :
        cell = str(int(r)+1) + g + b
        new_id = Litmus.cell[cell]['owner']['id']
        new_litmus = Litmus.db[new_id]
        adjacent.append({'id': new_id, 'case':'adjavent', 'litmus':new_litmus })
    if int(g) > 1 :
        cell = r + str(int(g)-1) + b
        new_id = Litmus.cell[cell]['owner']['id']
        new_litmus = Litmus.db[new_id]
        adjacent.append({'id': new_id, 'case':'adjavent', 'litmus':new_litmus })
    if int(g) < 8 :
        cell = r + str(int(g)+1) + b
        new_id = Litmus.cell[cell]['owner']['id']
        new_litmus = Litmus.db[new_id]
        adjacent.append({'id': new_id, 'case':'adjavent', 'litmus':new_litmus })
    if int(b) > 1 :
        cell = r + g + str(int(b)-1)
        new_id = Litmus.cell[cell]['owner']['id']
        new_litmus = Litmus.db[new_id]
        adjacent.append({'id': new_id, 'case':'adjavent', 'litmus':new_litmus })
    if int(b) < 8 :
        cell = r + g + str(int(b)+1)
        new_id = Litmus.cell[cell]['owner']['id']
        new_litmus = Litmus.db[new_id]
        adjacent.append({'id': new_id, 'case':'adjavent', 'litmus':new_litmus })
    if adjacent :
        thesaurus.update({'adjacent':{'count':len(adjacent), 'list':adjacent}})
    
    return thesaurus

def find_nearest(rgb, radius) :
    me = rgb
    neighbor = 1.0
    index = 0
    for litmus in Litmus.db:
        you = litmus['rgb']
        d = tuple(abs(you[i] - me[i]) for i in range(0,3))
        if d[0] < radius and d[1] < radius and d[2] < radius: 
            distance = (d[0]**2 + d[1]**2+ d[2]**2)**0.5
            if distance < neighbor :
                neighbor = distance
                index = litmus['id']
    return index

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


