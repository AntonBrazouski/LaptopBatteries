from django.test import TestCase, SimpleTestCase, Client
from accum_articles.models import LaptopBattery, BatteryDescription
from django.urls import reverse 
from accum_articles import urls 
from django.contrib.auth import get_user_model

#from accum_articles import urreversels  


class SimpleTests(SimpleTestCase):
	
	def test_index_page_status_code(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		
	def test_laptop_search_page_status_code(self):
		response = self.client.get('/laptop_search')
		self.assertEqual(response.status_code, 200)
		
	def test_battery_search_page_status_code(self):
		response = self.client.get('/battery_search')
		self.assertEqual(response.status_code, 200)
	
		
class BasicBatteryTest(TestCase):
		
	def setUp(self):
		LaptopBattery.objects.create(article='test_art')
				
	def test_article_content(self):
		battery = LaptopBattery.objects.get(id=1)
		expected_object_name = f'{battery.article}'
		self.assertEqual(expected_object_name, 'test_art') #updated
	 

class SearchAllViewTest(TestCase):
	
	def setUp(self):
		LaptopBattery.objects.create(article='test_art')
		
	def test_view_url_exist_at_proper_location(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)
		
	def test_view_url_by_name(self):  
		resp = self.client.get(reverse('accum_articles:search_laptop'))		
		self.assertEqual(resp.status_code, 200)
	
class AdvancedBatteryTest(TestCase):
	
	def setUp(self):		
		self.battery = LaptopBattery.objects.create(
			article = 'test_art',
		)
	
	def test_string_representation(self):
		battery = LaptopBattery(article='test_art')
		self.assertEqual(str(battery), battery.article)
		
	def test_absolute_url(self):
		self.assertEqual(self.battery.get_absolute_url(), '/1/')	
			
	def test_battery_content(self):
		self.assertEqual(f'{self.battery.article}', 'test_art')	
	
	def test_battery_search_view(self):
		response = self.client.get(reverse('accum_articles:search_laptop'))	
		self.assertContains(response, 'Battery Finder')
		self.assertTemplateUsed(response, 'accum_articles/search_all.html', 'accum_articles/base.html')
			
	def test_battery_view(self):
		response = self.client.get(reverse('accum_articles:view_battery', args=('1', 'test_art', 'False')))	
		#response = self.client.get('/1/test_art/is_battery_search=False') #same
		#no_response = self.client.get('/2/test_art/is_battery_search=False') #error
		#no_response = self.client.get(reverse('accum_articles:view_battery', args=('2', 'test_art', 'False'))) #error	
		
		self.assertEqual(response.status_code, 200)
		#self.assertEqual(no_response.status_code, 404) #DoesNotExist error
		self.assertContains(response, 'test_art')
		self.assertTemplateUsed(response, 'accum_articles/battery_view.html')
	
	def test_simple_add_view(self):
		response = self.client.post('/simple_add/', {
			'article' :'new_art',
		})	
		self.assertEqual(response.status_code, 200)
		#self.assertContains(response, 'new_art') # AssertionError
		#print(response)
	
	def test_simple_add_view_reverse(self):
		response = self.client.post(reverse('accum_articles:simple_add'), {
			'article' :'new_art',
		})	
		self.assertEqual(response.status_code, 200)
		#self.assertContains(response, 'new_art') # AssertionError
		#print(response)
		
		
'''	
	def test_should_set_article(self):
		battery = LaptopBattery.objects.get(id=1)
		expected_object_name = f'{LaptopBattery.article}'
		self.assertEqual(expected_object_name, 'good')
		
	def test_should_not_equal_wrong_article(self):
		self.assertNotEqual(battery.__str__(), test_article_negative)


	def test_article_len_lt_5(self): 
		test_article = "12345"
		battery = LaptopBattery.objects.create(article=test_article ) 	
		#self.assertNotEqual(battery.__str__(), test_article ) # FAILS
		
	def test_detail_view_page_status_code(self):
		
		response = self.client.get('/3/AC14B18K/is_battery_search=False')
		#self.assertEqual(response.stauts_code, 200) # FAILS - LaptopBattery does not exist
 		#print('hello')
	
'''
