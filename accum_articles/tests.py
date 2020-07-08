from django.test import TestCase, SimpleTestCase, Client
from accum_articles.models import LaptopBattery, BatteryDescription
from django.urls import reverse 
from accum_articles import urls 
from django.contrib.auth import get_user_model


class SimpleTests(SimpleTestCase):
	
	def test_index_page_status_code(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		
	def test_laptop_search_page_status_code(self):
		response = self.client.get('/laptop_search/')
		self.assertEqual(response.status_code, 200)


	def test_battery_search_page_status_code(self):
		response = self.client.get('/battery_search/')
		self.assertEqual(response.status_code, 200)


class AllViewsTests(TestCase):
	
	def setUp(self):
		LaptopBattery.objects.create(article='test_art')
		
	def test_view_index_url_exist_at_proper_location(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Battery Finder')
		self.assertTemplateUsed(response, 'accum_articles/battery_list_view.html', 'accum_articles/base.html')

		
	def test_view_search_laptop_url_by_name(self):  
		response = self.client.get(reverse('accum_articles:search_laptop'))		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Battery Finder')
		self.assertTemplateUsed(response, 'accum_articles/battery_list_view.html', 'accum_articles/base.html')


	def test_view_search_battery_url_by_name(self):  
		response = self.client.get(reverse('accum_articles:search_battery'))		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Battery Finder')
		self.assertTemplateUsed(response, 'accum_articles/battery_list_view.html', 'accum_articles/base.html')


	def test_view_battery_url_by_name(self):  
		response = self.client.get(reverse('accum_articles:detail_battery', args=(1, )))		
		self.assertEqual(response.status_code, 200)
		no_response = self.client.get(reverse('accum_articles:detail_battery', args=(2, ))) 	
		self.assertContains(response, 'test_art')
		self.assertTemplateUsed(response, 'accum_articles/battery_detail_view.html')
		self.assertEqual(no_response.status_code, 404) 


	def test_view_laptop_url_by_name(self):  
		response = self.client.get(reverse('accum_articles:detail_laptop', args=(1, )))		
		self.assertEqual(response.status_code, 200)
		no_response = self.client.get(reverse('accum_articles:detail_laptop', args=(2, ))) 	
		self.assertContains(response, 'test_art')
		self.assertTemplateUsed(response, 'accum_articles/battery_detail_view.html')
		self.assertEqual(no_response.status_code, 404) 
	
	def test_view_simple_admin_url_by_name(self):  
		response = self.client.get(reverse('accum_articles:simple_admin'))		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Welcome')
		self.assertTemplateUsed(response, 'accum_articles/simple_admin.html')
	
		
	def test_view_simple_add_url_by_name(self):
		response = self.client.post(reverse('accum_articles:simple_add'), {
			'article' :'new_art',
		})	
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'add description') 
		self.assertTemplateUsed(response, 'accum_articles/laptopbattery_form.html')

	def test_view_csv_add_by_name(self):
		response = self.client.get(reverse('accum_articles:csv_add'))	
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'csv') 
		self.assertTemplateUsed(response, 'accum_articles/csv_add.html')

	def test_view_csv_gen_by_name(self):
		response = self.client.get(reverse('accum_articles:csv_gen'))	
		self.assertEqual(response.status_code, 200)
		#self.assertContains(response, 'file') 
	
	def test_view_detail_by_name(self):
		response = self.client.get(reverse('accum_articles:detail_battery', args=('1'))) # ?? '1' - str ?
		no_response = self.client.get(reverse('accum_articles:detail_battery', args=('2'))) 	

		self.assertEqual(response.status_code, 200)
		self.assertEqual(no_response.status_code, 404) 
	 

	
class BatteryTest(TestCase):
	
	def setUp(self):		
		self.battery = LaptopBattery.objects.create(
			article = 'test_art',
		)
	
	def test_string_representation(self):
		battery = LaptopBattery(article='test_art')
		self.assertEqual(str(battery), battery.article)
		
	def test_should_set_article(self):
		expected_object_name = 'new_test'
		test_article_negative = 'bad_article'
		self.battery.article= expected_object_name
		self.assertEqual(self.battery.article, expected_object_name)
		self.assertNotEqual(self.battery.article, test_article_negative)
			
	def test_absolute_url(self):
		test_url_name = '/detail_battery/1/'
		self.assertEqual(self.battery.get_absolute_url(), test_url_name)

	def test_article_len_lte_8(self): 
			article_len_8 ='12345678'
			article_len_0 = ''
			article_none = None
			article_len_9 = '123456789'
			
			
			self.battery.article = article_len_8
			self.assertEqual(self.battery.article, article_len_8)
			self.battery.article = article_len_0
			self.assertEqual(self.battery.article, article_len_0)
			self.battery.article = article_none
			self.assertEqual(self.battery.article, article_none)
			self.battery.article = article_len_9
			#self.assertNotEqual(self.battery.article, article_len_9) # ??
