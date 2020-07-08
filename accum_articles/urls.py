from django.urls import path

from accum_articles import views


app_name = "accum_articles"

urlpatterns = [
	#class based views
	path("", views.BatteryListView.as_view(), {'is_battery_search': False}, name='search_laptop'),#CBV
	path("laptop_search/", views.BatteryListView.as_view(), {'is_battery_search': False}, name='search_laptop'), #CBV
	path('battery_search/', views.BatteryListView.as_view(),{'is_battery_search': True}, name='search_battery'), #CBV
	path('detail_battery/<int:pk>/', views.BatteryDetailView.as_view(),{'is_battery_search': True}, name='detail_battery'), #CBV
	path('detail_laptop/<int:pk>/', views.BatteryDetailView.as_view(),{'is_battery_search': False}, name='detail_laptop'), #CBV
	path("simple_admin/", views.AdminView.as_view(), name="simple_admin"), #CBV
	path("add/", views.BatteryCreate.as_view(), name="simple_add"), #CBV
	path("add_desc/", views.BatteryDescriptionCreate.as_view(), name="simple_add_desc"), #CBV
	path("csv_add/", views.CsvAddView.as_view(), name="csv_add"), #CBV


	#simle admin
	#path("simple_add/", views.simple_add, name='simple_add'),
	#path("simple_add_desc", views.simple_add_desc, name='simple_add_desc'),
	
	#csv_views
	#path("csv_add", views.csv_add, name='csv_add'),
	path("csv_gen", views.csv_gen, name='csv_gen'),
	path("csv_show", views.csv_show, name='csv_show'),


]
	
