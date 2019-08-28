from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import time
import os
import json
import math
from .litmus_database import Litmus
from .litmus_search import search_main, search_info
from .color_vector import ColorVector
from .litmus_plot import plot_RGB

def litmus(request):
    return redirect('litmus:main')

def main(request):
    if request.method == "POST":
        word = request.POST['search']
        search = search_main(word)
        if search:
            context = {'word':word, 'search':search}
            return render(request, 'litmus/color_search.html', context)
    context = {'count':'Normal'}
    return render(request, 'litmus/main.html', context)

def colorSearch(request):
    if request.method == "POST":
        word = request.POST['search']
        search = search_main(word)
        # word = 'something'
        if search:
            context = {'word':word, 'search':search}
            return render(request, 'litmus/color_search.html', context)
    context = {'count':'Normal'}
    return render(request, 'litmus/color_search.html', context)

def colorInfo(request, pk): 
    color_id = int(pk)
    litmus = Litmus.get_by_id(color_id)
    hexa = litmus['hexa']
    vector = ColorVector(hexa).all
    search = search_info(color_id)
    message = ""
    context = {'message':message, 'litmus':litmus, 'vector':vector, 'search':search}
    return render(request, 'litmus/color_info.html', context)

def colorLibrary(request):
    db = Litmus.classify_by_group('name', 'ascend')
    total = Litmus.count()
    context = {'colors':db, 'total':total}
    return render(request, 'litmus/color_library.html', context)
    