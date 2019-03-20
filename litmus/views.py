from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
import time
import os
import json
import math
from .litmus import Litmus

def litmus(request):
    return redirect('litmus:main')

def main(request):
    data = Litmus.data
    count = Litmus.count
    context = {'data':data, 'count':count}
    return render(request, 'litmus/main.html', context)

def colorSearch(request):
    return redirect('litmus:main')