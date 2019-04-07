from .litmus_database import Litmus
from .color_space import CVC

def search_color(word):
    radius = 0.1
    hexa = is_hexa(word)
    if hexa:
        search = search_by_hexa(hexa, radius)
    else:
        search = search_by_name(word)
    search.update({'supernova':{'count':len(Litmus.supernova), 'list':Litmus.supernova}})
    search.update({'giant':{'count':len(Litmus.giant), 'list':Litmus.giant}})
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
    sorted_i = sorted(identical, key=lambda i: i['litmus']['name'])
    sorted_n = sorted(neighbor, key=lambda n: n['distance'])
    return {'identical':{'count':len(sorted_i), 'list':sorted_i}, 'neighbor':{'count':len(sorted_n), 'list':sorted_n}}

def search_by_name(word):
    match = []
    for litmus in Litmus.db:
        name = litmus['name']
        if (word.lower() in name.lower()):
            match.append({'id': litmus['id'], 'case':'match', 'litmus':litmus})
    sorted_m = sorted(match, key=lambda m: m['litmus']['name'])
    return {'match':{'count':len(sorted_m), 'list':sorted_m}}

def is_hexa(word):
    if len(word) == 7 and word[0]=="#":
        hexa = word[1:7]
    elif len(word) == 6:
        hexa = word[0:6]
    else :
        return False
    try:
        int(hexa, 16)
        return '#'+ hexa
    except ValueError:
        return False

