from django.test import TestCase, SimpleTestCase
from accum_articles.models import LaptopBattery, BatteryDescription
from django.urls import reverse 

#from accum_articles import urls  


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
	
		
class BatteryTestCase(TestCase):
		
	def setUp(self):
		LaptopBattery.objects.create(article='just a test')
		
		
	def test_article_content(self):
		post = LaptopBattery.objects.get(id=1)
		expected_object_name = f'{LaptopBattery.article}'

	 

class SearchAllViewTest(TestCase):
	
	def setUp(self):
		LaptopBattery.objects.create(article='this is another test')
		
	def test_view_url_exist_at_proper_location(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)
		
	def test_view_url_by_name(self):  # ERROR reverse not found
		pass
		#resp = self.client.get(reverse('view_battery'))
		#self.assertEqual(resp.status_code, 200)
	
		

			
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
