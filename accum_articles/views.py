
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.template import loader

from django.views import View 
from django.views.generic import ListView
from .forms import ArticleForm
import csv
from accum_articles.models import LaptopBattery, BatteryDescription
from . import urls

class BatteryListView(ListView):

	model = LaptopBattery
	template_name = 'accum_articles/battery_list_view.html'
	is_battery_search = False  
		
	def get_context_data(self, **kwargs):          
		context = super().get_context_data(**kwargs)    	            
		context["is_battery_search"] = self.kwargs['is_battery_search']
		self.is_battery_search = context["is_battery_search"]
		
		context["search_result"] = self.get_queryset()
		
		return context	
						
	def get_queryset(self):	
		search_str = None
		search_result = None
		try:
			search_str = self.request.GET['search']
			if self.is_battery_search == False:					
				search_result = LaptopBattery.objects.filter(batterydescription__compatible_models__contains=search_str)
			else:
				search_result = LaptopBattery.objects.filter(article__contains = search_str)
		except:
			pass				
		
		return 	search_result	


class BatteryDetailView(DetailView):
	model = LaptopBattery
	template_name="accum_articles/battery_detail_view.html"
	context_object_name = "battery"
	is_battery_search = True
	battery_id = None
	
	def get_context_data(self, **kwargs):          
		context = super().get_context_data(**kwargs)    	            
		context["is_battery_search"] = self.kwargs['is_battery_search']
		self.is_battery_search = context["is_battery_search"]

		return context	

class AdminView(TemplateView):
	template_name = "accum_articles/simple_admin.html"

class BatteryCreate(CreateView):
	model = LaptopBattery
	fields = ['article', 'manufacturer']

class BatteryDescriptionCreate(CreateView):
	model = BatteryDescription
	fields = ['battery', 'compatible_articles', 'compatible_models']
		
	
	
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


class CsvAddView(TemplateView):
	template_name = "accum_articles/csv_add.html"
	
	def post(self, request):
		afile = None
		line_count = None
		error_message = None			
		#print(request.POST)
		#print(request.FILES) 		
		if request.FILES != {}:
			afile = request.FILES['file']
			print(afile) 
		csv_len = 14
		line_count = 12
		error_message = 'error'
		return render( 
			request, 'accum_articles/csv_add.html',
				{
				'csv_len':csv_len,  
				'line_count':line_count,
				 'error_message':error_message 
				}
			)	
		
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
