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

def litmus(request):
    return redirect('litmus:main')

def main(request):
    if request.method == "POST":
        word = request.POST['search']
        if len(word):
            hexa = is_hexa(word)
            radius = 0.1
            if hexa:
                search = search_by_hexa(hexa, radius)
                count = {'identicals':len(search['identicals']), 'neighbors':len(search['neighbors'])}
            else:
                search = search_by_name(word)
                count = {'matches':len(search['matches'])}
            context = {'word':word, 'search':search, 'count':count}
            return render(request, 'litmus/color_search.html', context)

    data = Litmus.data
    count = Litmus.count
    context = {'data':data, 'count':count}
    return render(request, 'litmus/main.html', context)

def colorSearch(request):
    word = ""
    search = {}
    if request.method == "POST":
        word = request.POST['search']
        if len(word):
            hexa = is_hexa(word)
            if hexa:
                radius = 0.1
                search = search_by_hexa(hexa, radius)
            else:
                search = search_by_name(word)
    context = {'word':word, 'search':search}
    return render(request, 'litmus/color_search.html', context)

def colorInfo(request, pk):
 
    # url_string = resolve_url('litmus:colorInfo', id=pk)
    # litmus = get_object_or_404(Litmus, id=pk)
    # vector = ColorVector(litmus['hexa'])
    context = {'pk':pk}
    return render(request, 'litmus/color_info1.html', context)