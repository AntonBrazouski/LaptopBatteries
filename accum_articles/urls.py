from django.urls import path

from accum_articles import views


app_name = "accum_articles"

urlpatterns = [
	#class based views
	path("", views.BatteryListView.as_view(), 
		{'is_battery_search': False}, name='search_laptop'),
	path("laptop_search/", views.BatteryListView.as_view(),
		{'is_battery_search': False}, name='search_laptop'), 
	path('battery_search/', views.BatteryListView.as_view(),
		{'is_battery_search': True}, name='search_battery'), 
	path('detail_battery/<int:pk>/', views.BatteryDetailView.as_view(),
		{'is_battery_search': True}, name='detail_battery'), 
	path('detail_laptop/<int:pk>/', views.BatteryDetailView.as_view(),
		{'is_battery_search': False}, name='detail_laptop'), 
	path("simple_admin/", views.AdminView.as_view(),
		name="simple_admin"), 
	path("add/", views.BatteryCreate.as_view(), name="simple_add"), 
	path("add_desc/", views.BatteryDescriptionCreate.as_view(), 
		name="simple_add_desc"), 
	path("csv_add/", views.CsvAddView.as_view(), name="csv_add"), 
	path("csv_gen/", views.CsvGenView.as_view(), name="csv_gen"), 

]
	
