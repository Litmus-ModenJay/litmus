from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from datetime import datetime
import time
import os
import json
import math
from .litmus_db import Litmus
from .litmus_search import is_hexa, search_by_hexa, search_by_name
from .color_vector import ColorVector
from .litmus_plot import plotRGB

def litmus(request):
    return redirect('litmus:main')

def main(request):
    if request.method == "POST":
        word = request.POST['search']
        if len(word):
            hexa = is_hexa(word)
            if hexa:
                search = search_by_hexa(name, hexa, radius=0.1, exclude_me=False)
            else:
                search = search_by_name(word)
            plot = plotRGB(search['plot'])
            context = {'word':word, 'search':search, 'plot':plot}
            return render(request, 'litmus/color_search.html', context)

    data, count = Litmus.data, Litmus.count
    context = {'data':data, 'count':count}
    return render(request, 'litmus/main.html', context)

def colorSearch(request):
    search = {}
    plot = {}
    word = ""
    if request.method == "POST":
        word = request.POST['search']
        if len(word):
            hexa = is_hexa(word)
            if hexa:
                search = search_by_hexa(hexa, radius=0.1)
            else:
                search = search_by_name(word)
            plot = plotRGB(search['plot'])
    context = {'word':word, 'search':search, 'plot':plot}
    return render(request, 'litmus/color_search.html', context)

def colorInfo(request, pk): 
    id = int(pk)
    litmus = Litmus.get_by_id(id)
    hexa = litmus['hexa']
    vector = ColorVector(hexa).all
    search = search_by_hexa(hexa, radius=0.1)
    plot = plotRGB(search['plot'])
    message = ""
    context = {'message':message, 'litmus':litmus, 'vector':vector, 'search':search, 'plot':plot}
    return render(request, 'litmus/color_info.html', context)

def colorLibrary(request):
    return render(request, 'litmus/color_library.html')