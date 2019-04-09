from .litmus_database import Litmus
from .color_space import CVC

def search_main(word):
    if len(word) < 3: # 2글자 이하는 검색에서 제외
        return {}
    search = {}
    if word[0] == '#':
        tag = word[1:]
        hexa = is_hexa(tag) # 헥사코드인지 확인 - #시작 16진 7 숫자 (#FFFFFF) or 16진 6 숫자 (FFFFFF)
        if hexa: 
            search = search_by_hexa(hexa, radius=0.1)
        else:
            category = is_tag(tag) # 키워드인지 확인 - #Family or #Keyword
            if category == 'family':
                search = search_by_family(tag)
            elif category == 'keyword':
                search = serch_by_keyword(tag)
    elif word[0] == '@':
        geo = is_geo(word[1:])
        if geo:
            search = search_by_geo(geo, radius = 10)
    else:
        search = search_by_name(word)
    if search:
        # 디폴트 리스트를 검색 결과에 추가 (supernova & giant)
        search.update({'supernova':{'count':len(Litmus.supernova), 'list':Litmus.supernova}})
        # search.update({'giant':{'count':len(Litmus.giant), 'list':Litmus.giant}})
    return search

def search_info(my_id, hexa):
    search = search_by_hexa(hexa, radius=0.1)
    for item in search['identical']['list']:
        if my_id == item['id']:
            item['case'] = 'self'
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
    for litmus in Litmus.db:
        for item in litmus['family']:
            if tag == item:
                family.append({'id': litmus['id'], 'case':'family', 'litmus':litmus})
    if family:
        sorted_f = sorted(family, key=lambda f: f['litmus']['name'])
        return {'family':{'count':len(sorted_f), 'list':sorted_f}}
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

def is_tag(tag):
    # tag 가 Litmus.giant 에 속하는지 검색
    for star in Litmus.giant:
        if tag == star['litmus']['name']:
            return 'family'
    """
    # tag 가 Litmus.keyword 에 속하는지 검색
    for word in Litmus.keyword:
        if tag == word:
            return 'keyword'
    """
    return ''

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


