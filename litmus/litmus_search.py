from .litmus_database import Litmus
from .color_space import CVC

def search_color(word):
    radius = 0.1
    hexa = is_hexa(word)
    if hexa:
        search = search_by_hexa(hexa, radius)
    else:
        search = search_by_name(word)
    return search

def search_by_hexa(hexa, radius):
    me = CVC.hexa_rgb(hexa)
    identicals = []
    neighbors = []
    plotRGBdata = []
    for litmus in Litmus.db:
        you = litmus['rgb']
        d = tuple(abs(you[i] - me[i]) for i in range(0,3))
        if d[0] < radius and d[1] < radius and d[2] < radius: 
            distance = (d[0]**2 + d[1]**2+ d[2]**2)**0.5
            if distance < 0.0001 :
                identicals.append({'name':litmus['name'], 'hexa':litmus['hexa'], 'id':litmus['id'], 'distance':distance})
                plotRGBdata.append({'x':you[0], 'y':you[1], 'z': you[2], 'name':litmus['name'], 'hexa':litmus['hexa'], 'case':'identicals'})
            elif distance < radius:
                neighbors.append({'name':litmus['name'], 'hexa':litmus['hexa'], 'id':litmus['id'], 'distance':distance})
                plotRGBdata.append({'x':you[0], 'y':you[1], 'z': you[2], 'name':litmus['name'], 'hexa':litmus['hexa'], 'case':'neighbors'})
    sorted_i = sorted(identicals, key=lambda i: i['name'])
    sorted_n = sorted(neighbors, key=lambda n: n['distance'])
    return {'identicals':{'count':len(sorted_i), 'list':sorted_i}, 'neighbors':{'count':len(sorted_n), 'list':sorted_n}, 'plot':plotRGBdata}

def search_by_name(word):
    matches = []
    plotRGBdata = []
    for litmus in Litmus.db:
        name = litmus['name']
        if (word.lower() in name.lower()):
            matches.append({'name':litmus['name'], 'hexa':litmus['hexa'], 'id':litmus['id']})
            plotRGBdata.append({'x':litmus['rgb'][0], 'y':litmus['rgb'][1], 'z': litmus['rgb'][2], 'name':litmus['name'], 'hexa':litmus['hexa'], 'case':'matches'})
    sorted_m = sorted(matches, key=lambda m: m['name'])
    return {'matches':{'count':len(sorted_m), 'list':sorted_m}, 'plot':plotRGBdata}

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

