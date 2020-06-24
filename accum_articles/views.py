
from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from accum_articles.models import LaptopBattery, BatteryDescription

from django.views.generic.edit import CreateView

import csv


# Create your views here.

def index(request):
	return render(request, 'accum_articles/search_all.html' )


'''
def search_all(request, is_battery_search=True, search='', search_result=''):
	
	#if request.method == 'POST':
	#	search = request.POST['search']
	search = request.GET['search']
	
		if search != '':	
			if is_battery_search:
				search_result = LaptopBattery.objects.filter(article__contains=search)
				
			else: # search by laptop model instead 
				search_result = LaptopBattery.objects.filter(batterydescription__compatible_models__contains=search)
	
		else: # empty search
			search_result = None
				
	#else: # request.method == 'GET'
	#	search_result = None
		
	context = { "search" : search, "search_result": search_result, "is_battery_search": is_battery_search}		
	
	return render(request, 'accum_articles/search_all.html', context)
'''
	
def search_all(request, is_battery_search=True, search='', search_result=''):
	
	if request.method == 'POST':
		search = request.POST['search']
					
		if search != '':	
			if is_battery_search:
				search_result = LaptopBattery.objects.filter(article__contains=search)
				
			else: # search by laptop model instead 
				search_result = LaptopBattery.objects.filter(batterydescription__compatible_models__contains=search)
				
	else: # request.method == 'GET'
		search_result = None
		
	context = { "search" : search, "search_result": search_result, "is_battery_search": is_battery_search}		
	
	return render(request, 'accum_articles/search_all.html', context)

def view_battery(request, article, id, is_battery_search):
	battery = LaptopBattery.objects.get(id=id)	
	context = {"battery": battery, "is_battery_search":is_battery_search}
	
	return render(request, 'accum_articles/battery_view.html', context)
	

def simlpe_view_battery(request, id):
	battery = LaptopBattery.objects.get(id=id)	
	context = {"battery": battery}
	
	return render(request, 'accum_articles/battery_view.html', context)

	
def simlpe_view_battery_desc(request, id):
	
	battery = LaptopBattery.objects.get(id=id)	
	context = {"battery": battery}
	
	return render(request, 'accum_articles/battery_view.html', context)
	
def simple_add(request):
	article = None
	context = {}
	context["manufacturers_list"]=LaptopBattery.MANUFACTURER_CHOICES
	
	if request.method == 'POST':
		article = request.POST['article']
		new_battery = LaptopBattery.objects.create(article=article)
		context ["battery"]= new_battery
		context["created"]= True
		print(context)
		
		return render(request, 'accum_articles/simple_create.html', context)
		#return HttpResponseRedirect(reverse('accum_articles:simple_add'),context) # context doesn't work
			
	return render(request, 'accum_articles/simple_create.html', context)
	
def simple_add_desc(request):
	selected_id = None
	context = {}
	batteries = LaptopBattery.objects.all()
	context["batteries_list"] = LaptopBattery.objects.all()
	
	context["batteries_without_description"] = False
	for battery in batteries:
		try:
			if battery.batterydescription:
				pass
		except:
			context["batteries_without_description"] = True
			print(battery.id)
	
	if request.method == 'POST':
		selected_id = request.POST['battery_id']
		selected_battery = LaptopBattery.objects.get(id=selected_id)
		selected_compatible_models = request.POST['compatible_models']
		selected_compatible_articles = request.POST['compatible_articles']
		
		new_description = BatteryDescription.objects.create(battery=selected_battery)
		new_description.compatible_models = selected_compatible_models
		new_description.compatible_articles = selected_compatible_articles
		new_description.save() # prevents TypeError
		context["description"]= new_description
		context["created"] = True
		print(context)		
		
		return render(request, 'accum_articles/simple_create_desc.html', context)
		#return HttpResponseRedirect(reverse('accum_articles:simple_add_desc'), context) # context doesn't work
		
	return render(request, 'accum_articles/simple_create_desc.html', context)
	

def simple_admin(request):
	
	return render(request, 'accum_articles/simple_admin.html')
	
def handle_uploaded_file(f):
	
	try:
		with open('accum_articles/csv/batteries.csv', 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
	except:
		print('error')

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
		
def csv_add(request):
	if request.method == 'POST':
		afile = None
		line_count = None
		error_message = None
		
			
		#print(request.POST)
		#print(request.FILES) 
		
		if request.FILES != {}:
			afile = request.FILES['file']  
		
		if afile != None:		
			handle_uploaded_file(afile) # store uploaded file to batteries.csv				  	
			afile = "accum_articles/csv/batteries.csv"	
			csv_len = file_len(afile)
			
			try:
				with open(afile) as csv_file:
					csv_reader = csv.reader(csv_file, delimiter=',')
					line_count = 0
					headers = []
					batteries = []
					
					for row in csv_reader:
						if line_count == 0:
							headers = row
							line_count += 1
						else:
							batteries.append(row)
							LaptopBattery.objects.create(article=row[1], manufacturer=row[2])
							line_count += 1
			except:
				error_message = 'an error has occured during the file processing' 
				print('error')
						
		return render( 
			request, 'accum_articles/csv_add.html',
				{
				'csv_len':csv_len,  
				'line_count':line_count,
				 'error_message':error_message 
				}
			)
		
	return render(request, 'accum_articles/csv_add.html')
