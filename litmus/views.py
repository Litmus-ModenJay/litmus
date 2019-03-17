from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
import time
import os
import json
import math
from .litmus import LitmusDB

def litmus(request):
    return redirect('litmus:litmusHome')

def litmusHome(request):
    base = {'nav_home':'active', 'title':"Home", 'year':datetime.today().year}
    data = LitmusDB.all()
    count = LitmusDB.count()
    context = {'base':base, 'data':data, 'count':count}
    return render(request, 'litmus/home.html', context)
