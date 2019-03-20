from .litmus_db import Litmus
from .color_space import CVC


def search_by_hexa(hexa, radius):
    me = CVC.hexa_rgb(hexa)
    identicals = []
    neighbors = []
    for litmus in Litmus.data():
        you = litmus['rgb']
        d = tuple(abs(you[i] - me[i]) for i in range(0,3))
        if d[0] < radius and d[1] < radius and d[2] < radius: 
            distance = (d[0]**2 + d[1]**2+ d[2]**2)**0.5
            if distance < 0.0001 :
                identicals.append({'name':litmus['name'], 'hexa':litmus['hexa'], 'id':litmus['id'], 'distance':distance})
            elif distance < radius:
                neighbors.append({'name':litmus['name'], 'hexa':litmus['hexa'], 'id':litmus['id'], 'distance':distance})
    sorted_i = sorted(identicals, key=lambda i: i['name'])
    sorted_n = sorted(neighbors, key=lambda n: n['distance'])
    return {'identicals':{'count':len(sorted_i), 'list':sorted_i}, 'neighbors':{'count':len(sorted_n), 'list':sorted_n}}

def search_by_name(word):
    matches = []
    for litmus in Litmus.data():
        name = litmus['name']
        if (word.lower() in name.lower()):
            matches.append({'name':litmus['name'], 'hexa':litmus['hexa'], 'id':litmus['id']})
    sorted_m = sorted(matches, key=lambda m: m['name'])
    return {'matches':{'count':len(sorted_m), 'list':sorted_m}}

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

