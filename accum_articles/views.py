
from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from accum_articles.models import LaptopBattery, BatteryDescription

from django.views.generic.edit import CreateView
from django.views.generic import DetailView

import csv

from django.template import loader

from .forms import ArticleForm

# Create your views here.

def index(request):
	return render(request, 'accum_articles/search_all.html' )


#try CBV - ListView - Search all

from django.views.generic import ListView

#test

class BatteryListView(ListView):
	model = LaptopBattery
	template_name = 'accum_articles/battery_list_view.html'
	context_object_name = 'batteries_list'
	queryset = LaptopBattery.objects.filter(pk__lt = 10) #test
	is_battery_search = True # hardcoded
	
	def get(self, request, *args, **kwargs):
		is_battery_search = True # hardcoded
		model = LaptopBattery
		template_name = 'accum_articles/battery_list_view.html'
		context_object_name = 'batteries_list'
		queryset = LaptopBattery.objects.filter(pk__lt = 10)
		is_battery_search = True # hardcoded	
		return render(request, self.template_name, {
			'is_battery_search': is_battery_search,
		
		})
		
	# try context
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		return context
	
			
	''' new way
	def get(self, request, *args, **kwargs):
		is_battery_search = False # hardcoded
		
		try:
			search = request.GET['search']
		except:
			search=''
		
		if search != '':	
			if is_battery_search:
				search_result = LaptopBattery.objects.filter(article__contains=search)
			else: # search by laptop model instead 
				search_result = LaptopBattery.objects.filter(batterydescription__compatible_models__contains=search)	
		else: # empty search
			search_result = None
				
		
		return render(request, self.template_name, {
			'is_battery_search': is_battery_search,
			'search': search,
			'search_result': search_result,
			#'batteries_list': 'hello',
			
			})
	
	'''
	#form = self.form_class(initial=self.initial)
	
	
	''' old stuff
	try:
		search = request.GET['search']
	except:
		search=''
			
	if search != '':	
		if is_battery_search:
			search_result = LaptopBattery.objects.filter(article__contains=search)
			
		else: # search by laptop model instead 
			search_result = LaptopBattery.objects.filter(batterydescription__compatible_models__contains=search)
	
	else: # empty search
		search_result = None
					
	context = { "search" : search, "search_result": search_result, "is_battery_search": is_battery_search}		
	''' 




# search - GET requset
def search_all(request, is_battery_search=True, search='', search_result=''):
	try:
		search = request.GET['search']
	except:
		search=''
			
	if search != '':	
		if is_battery_search:
			search_result = LaptopBattery.objects.filter(article__contains=search)
			
		else: # search by laptop model instead 
			search_result = LaptopBattery.objects.filter(batterydescription__compatible_models__contains=search)

	else: # empty search
		search_result = None
					
	context = { "search" : search, "search_result": search_result, "is_battery_search": is_battery_search}		
	
	return render(request, 'accum_articles/search_all.html', context)

''' using POST
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
'''

def view_battery(request, article, id, is_battery_search):
	battery = LaptopBattery.objects.get(id=id)	
	context = {"battery": battery, "is_battery_search":is_battery_search}
	
	return render(request, 'accum_articles/battery_view.html', context)

class BatteryDetailView(DetailView):
	model = LaptopBattery
	template_name="accum_articles/battery_detail_view.html"
	context_object_name = "battery"

	#test
	def get_context_data(self, **kwargs):          
		context = super().get_context_data(**kwargs)                     
		new_context_entry = "here it goes"
		context["new_context_entry"] = new_context_entry
		return context
		
''' unused views
def simlpe_view_battery(request, id):
	battery = LaptopBattery.objects.get(id=id)	
	context = {"battery": battery}
	
	return render(request, 'accum_articles/battery_view.html', context)

	
def simlpe_view_battery_desc(request, id):
	
	battery = LaptopBattery.objects.get(id=id)	
	context = {"battery": battery}
	
	return render(request, 'accum_articles/battery_view.html', context)
'''

''' # using manual form 
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
'''

# using form validation
def simple_add(request): 
	article = None
	context = {}
	context["manufacturers_list"]=LaptopBattery.MANUFACTURER_CHOICES
	
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			
			#article = form.fields.article #request.POST['article']
			article = form.cleaned_data['article'] # works fine
			manufacturer = form.cleaned_data['manufacturer']
			new_battery = LaptopBattery.objects.create(article=article, manufacturer=manufacturer)
			context ["battery"]= new_battery
			context ["battery"]= new_battery
			
			context["created"]= True
			#print(context)
			form = ArticleForm()
			context['form'] = form
			
		return render(request, 'accum_articles/simple_create.html',  context )
		#return HttpResponseRedirect(reverse('accum_articles:simple_add'),context) # context doesn't work
	else: #GET
		form = ArticleForm()
		context['form'] = form 	
		print(context)	
	return render(request, 'accum_articles/simple_create.html',  context)

	
def simple_add_desc(request):
	selected_id = None
	context = {}
	context["batteries_list"] = LaptopBattery.objects.filter(batterydescription__isnull=True)

	#VL FIX
	context["batteries_without_description"] = LaptopBattery.objects.filter(batterydescription__isnull=True).exists()
	
	
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
		context["batteries_without_description"] = LaptopBattery.objects.filter(batterydescription__isnull=True).exists()
		
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

def csv_gen(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="batteries.csv"'

    writer = csv.writer(response)
    counter = 0
    for article in list(LaptopBattery.objects.all()):
	    counter += 1 
	    writer.writerow([counter, article])

    return response
    

def csv_show(request):
    # Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="batteries.csv"'
	
	csv_data = list(LaptopBattery.objects.all())
	print(csv_data)
	
	t = loader.get_template('accum_articles/csv_show.html')
	c = {'data':csv_data}
	response.write(t.render(c))
	
	return response
