from django.db import models
from django.urls import reverse
#from accum_articles import urls 

# Create your models here.
		
class LaptopBattery(models.Model):
	
	MANUFACTURER_CHOICES = [
		('NoName' , 'Unknown'),
		('Hewlett Packard' , 'HP'),
		('ACER' , 'ACER'),
	]
		
	article = models.CharField(max_length=8)
	manufacturer = models.CharField(max_length=16, choices= MANUFACTURER_CHOICES, default= 'NoName')

	def __str__(self):
		return self.article 
		
	def get_absolute_url(self):
		return reverse('accum_articles:detail_battery', args=[str(self.id)])
  
  
class BatteryDescription(models.Model):
	
	compatible_articles = models.CharField(max_length=24, null=True)
	compatible_models = models.TextField(null=True)
	battery = models.OneToOneField(LaptopBattery, on_delete = models.CASCADE)
	
	def __str__(self):
		return  self.compatible_models 
	
	def get_absolute_url(self):
		return reverse('accum_articles:detail_battery', args=[str(self.battery.id)])
	
