from django.urls import path

from accum_articles import views


app_name = "accum_articles"

urlpatterns = [
	#search views
	path("", views.search_all, {'is_battery_search': False}, name='search_laptop'),
	path("laptop_search", views.search_all, {'is_battery_search': False}, name='search_laptop'),
	path("battery_search", views.search_all, {'is_battery_search': True}, name='search_battery'),
	
		
	
	#detail view
	path("<int:id>/<str:article>/is_battery_search=<is_battery_search>", views.view_battery, name='view_battery'),
			
	#simle admin
	path("simple_admin", views.simple_admin, name='simple_admin'),
	path("simple_add/", views.simple_add, name='simple_add'),
	path("simple_add_desc", views.simple_add_desc, name='simple_add_desc'),
	
	#csv_views
	path("csv_add", views.csv_add, name='csv_add'),
	path("csv_gen", views.csv_gen, name='csv_gen'),
	path("csv_show", views.csv_show, name='csv_show'),
	
	#class based views
	#path('laptop_search', views.BatteryListView.as_view(),{'is_battery_search': True}, name='search_laptop'), #CBV
	path('<int:pk>/', views.BatteryDetailView.as_view(), name='detail'),
	
]
	
