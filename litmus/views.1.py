from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
import time
import os
import json
import math
from .models import ColorDB
from .forms import ColorRegisterForm
from .color import ColorIndex, is_hexa
from .plots import plot1d, plotRGB

def library(request):
    return redirect('library:colorList')
    
def colorList(request):
	litmus = {}
	total = ColorDB.objects.count()
	for item in ColorDB.GROUP_CHOICES :
		key = item[0]
		queryset = ColorDB.objects.filter(group=key).order_by('name')
		value = {'total': len(queryset), 'queryset': queryset}
		litmus.update({key:value})

	base = {'nav_library': 'active','title': "Library",'year': datetime.today().year}
	context = {'base': base, 'colors': litmus, 'total':total}
	return render(request, 'library/color_list.html', context)

def colorSearch(request):
	search = {}
	total = {}
	word = ""
	if request.method == "POST":
		word = request.POST['search']
		if len(word)  :
			hexa = ""
			identicals = []
			neighbors = []
			substrings = []
			if is_hexa(word):
				hexa = is_hexa(word)
				index = ColorIndex(hexa)
				colors = ColorDB.objects.all()
				for color in colors:
					compare = ColorIndex(color.hexa)
					del_r = abs(index.rgb['norm']['r']-compare.rgb['norm']['r'])
					del_g = abs(index.rgb['norm']['g']-compare.rgb['norm']['g'])
					del_b = abs(index.rgb['norm']['b']-compare.rgb['norm']['b'])
					if del_r <0.1 and del_g <0.1 and del_b <0.1 : 
						distance = math.sqrt(del_r*del_r + del_g*del_g + del_b*del_b)
						if distance < 0.0001 :
							identicals.append({'name':color.name, 'hexa':color.hexa, 'pk':color.pk, 'distance':distance})
						elif distance < 0.1:
							neighbors.append({'name':color.name, 'hexa':color.hexa, 'pk':color.pk, 'distance':distance})
			else :
				colors = ColorDB.objects.all()
				word_lower = word.lower()
				for color in colors:
					name_lower = color.name.lower()
					# if name_lower.find(search_lower) and len(substrings)<120 :
					if (word_lower in name_lower) :
						substrings.append({'name':color.name, 'hexa':color.hexa, 'pk':color.pk})

			sorted_identicals = sorted(identicals, key=lambda i: i['name'])
			sorted_neighbors = sorted(neighbors, key=lambda n: n['distance'])
			sorted_substrings = sorted(substrings, key=lambda s: s['name'])

			search = {'identicals': sorted_identicals, 'neighbors': sorted_neighbors, 'substrings': sorted_substrings}
			total = {'identicals': len(identicals), 'neighbors': len(neighbors), 'substrings': len(substrings)}
	
	base = {'nav_library': 'active','title': "Library",'year': datetime.today().year}
	context = {'base': base, 'colors': search, 'total':total, "word": word }
	return render(request, 'library/color_search.html', context)

def colorRegister(request):
	message = ''
	form = ColorRegisterForm() # Clear fields
	if request.method == "POST":
		form = ColorRegisterForm(request.POST)
		if form.is_valid(): 
			color = form.save(commit=False)
			color.name = form.cleaned_data['name']
			color.hexa = form.cleaned_data['hexa'].upper()
			color.save()
			# Get color index
			color_index = ColorIndex(color.hexa)
			# Save Litmus with color group
			litmus = ColorDB.objects.get(name=color.name) # 차후 ColorDB 클래스 명칭을 Litmus 로 변경
			litmus.group = color_index.group
			litmus.depth = color_index.depth
			# param = color_index.rgb['param']
			# litmus.intensity = color_index.rgb['param']['i']
			litmus.save()
			
			message = 'REGISTER_COLOR'
			base = {'nav_library': 'active','title': "Library",'year': datetime.today().year}
			context = {'base': base, 'message': message, 'litmus': litmus, 'index': color_index}
			return render(request, 'library/color_info.html', context)
		
	# colors = ColorDB.objects.all()
	base = {'nav_library': 'active','title': 'Library','year': datetime.today().year}
	context = {'base': base, 'form': form}
	# context = {'base': base, 'colors': colors}
	return render(request, 'library/color_register.html', context)
	
def colorInfo(request, pk):
	message = ''
	litmus = get_object_or_404(ColorDB, pk=pk)
	index = ColorIndex(litmus.hexa)
	# Search Colors
	identicals = []
	neighbors = []
	plotRGBdata = []
	plotRGBdata.append({'x':index.rgb['norm']['r'], 'y':index.rgb['norm']['g'], 'z': index.rgb['norm']['b'], 'name':litmus.name, 'hexa': litmus.hexa, 'case':'self'})
	
	colors = ColorDB.objects.all()
	for color in colors:
		if not litmus.name == color.name :
			compare = ColorIndex(color.hexa)
			del_r = abs(index.rgb['norm']['r']-compare.rgb['norm']['r'])
			del_g = abs(index.rgb['norm']['g']-compare.rgb['norm']['g'])
			del_b = abs(index.rgb['norm']['b']-compare.rgb['norm']['b'])
			if del_r <0.1 and del_g <0.1 and del_b <0.1 : 
				distance = math.sqrt(del_r*del_r + del_g*del_g + del_b*del_b)
				if distance < 0.0001 :
					identicals.append({'name':color.name, 'hexa':color.hexa, 'pk':color.pk, 'distance':distance})
					plotRGBdata.append({'x':compare.rgb['norm']['r'], 'y':compare.rgb['norm']['g'], 'z': compare.rgb['norm']['b'], 'name':color.name, 'hexa': color.hexa, 'case':'identicals'})
				elif distance < 0.10:
					neighbors.append({'name':color.name, 'hexa':color.hexa, 'pk':color.pk, 'distance':distance})
					plotRGBdata.append({'x':compare.rgb['norm']['r'], 'y':compare.rgb['norm']['g'], 'z': compare.rgb['norm']['b'], 'name':color.name, 'hexa': color.hexa, 'case':'neighbors'})
	sorted_identicals = sorted(identicals, key=lambda i: i['name'])
	sorted_neighbors = sorted(neighbors, key=lambda n: n['distance'])

	search = {'identicals': sorted_identicals, 'neighbors': sorted_neighbors}
	total = {'identicals': len(identicals), 'neighbors': len(neighbors)}
	# plot = plot1d()
	plot = plotRGB(plotRGBdata)

	base = {'nav_library': 'active','title': "Library",'year': datetime.today().year}
	context = {'base': base, 'message': message, 'litmus': litmus, 'index': index, 'colors': search, 'total':total, 'plot': plot}
	return render(request, 'library/color_info.html', context)

def colorDelete(request, pk):
	color = get_object_or_404(ColorDB, pk=pk)
	color.delete()
	return redirect('library:colorList')

def colorInitialize(request):
	litmus = ColorDB.objects.all()
	litmus.delete()
	
	with open("library/litmus_default.json") as f:
		dj = json.loads(f.read())

	for item in dj['Default']:
		name=item['name'].lower()
		hexa=item['index'][1:]
		color_index = ColorIndex(hexa)
		newcolor = ColorDB.objects.create(name=name, hexa=hexa, group=color_index.group, depth=color_index.depth)
	return redirect('library:colorList')

def colorBackup(request):
	litmus = ColorDB.objects.all()
	backup = []
	for item in litmus:
		name=item.name
		hexa=item.hexa
		backup.append({'name':name, 'index':'#'+hexa})
	with open("library/litmus_backup.json", 'w') as json_file:
		json.dump({'Default':backup}, json_file, indent = 4, sort_keys=True)
	return redirect('library:colorList')