from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import time
import os
import json
import math
from .litmus_database import Litmus
from .litmus_search import is_hexa, search_by_hexa, search_by_name
from .color_vector import ColorVector
from .litmus_plot import plot_RGB
from .ms_login import MSlogin
from .ms_auth import url_sign_in, url_sign_out, get_token_from_code, get_access_token
from .ms_graph import get_me 

def litmus(request):
    # 메인 페이지 처음 렌더 시 로그인 redirect 변수를 제공해야 함.
    uri_in = request.build_absolute_uri(reverse('litmus:msLogin'))
    uri_out = request.build_absolute_uri(reverse('litmus:msLogout'))
    sign_in = url_sign_in(uri_in)
    sign_out = url_sign_out(uri_out)
    MSlogin.redirect = {'login':uri_in, 'logout': uri_out}
    MSlogin.urls = {'login':sign_in, 'logout': sign_out}
    return redirect('litmus:main')

def main(request):
    
    if request.method == "POST":
        word = request.POST['search']
        if len(word):
            hexa = is_hexa(word)
            if hexa:
                search = search_by_hexa(hexa, radius=0.1)
            else:
                search = search_by_name(word)
            plot = plot_RGB(search)
            check_login = MSlogin.check(user_id=request.COOKIES.get('id'))
            context = {'login':check_login, 'word':word, 'search':search, 'plot':plot}
            return render(request, 'litmus/color_search.html', context)
    
    check_login = MSlogin.check(user_id=request.COOKIES.get('id'))
    context = {'count':check_login['status'], 'login':check_login}
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
            plot = plot_RGB(search)
    check_login = MSlogin.check(user_id=request.COOKIES.get('id'))
    context = {'login':check_login, 'word':word, 'search':search, 'plot':plot}
    return render(request, 'litmus/color_search.html', context)

def colorInfo(request, pk): 
    color_id = int(pk)
    litmus = Litmus.get_by_id(color_id)
    hexa = litmus['hexa']
    vector = ColorVector(hexa).all
    search = search_by_hexa(hexa, radius=0.1)
    plot = plot_RGB(search)
    message = ""
    check_login = MSlogin.check(user_id=request.COOKIES.get('id'))
    context = {'login':check_login, 'message':message, 'litmus':litmus, 'vector':vector, 'search':search, 'plot':plot}
    return render(request, 'litmus/color_info.html', context)

def colorLibrary(request):
    db = Litmus.classify_by_group('name', 'ascend')
    total = Litmus.count()
    check_login = MSlogin.check(user_id=request.COOKIES.get('id'))
    context = {'login':check_login, 'colors':db, 'total':total}
    return render(request, 'litmus/color_library.html', context)
    
def msLogin(request):
    code = request.GET['code']
    user_id = MSlogin.sign_in(code)
    # Set Cookie
    response = HttpResponseRedirect('/litmus/main')
    response.set_cookie('id', user_id)
    return response
    
def msLogout(request):
    user_id = request.COOKIES.get('id')
    MSlogin.status = 'logout'
    del MSlogin.users[user_id]
    return redirect('/litmus/main')