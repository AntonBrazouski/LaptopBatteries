from django import forms
from .models import LaptopBattery

class ArticleForm(forms.Form):
	MANUFACTURER_CHOICES = [
		('NoName' , 'Unknown'),
		('Hewlett Packard' , 'HP'),
		('ACER' , 'ACER'),
	]
	
	article = forms.CharField(label = 'Article', max_length=8)
	manufacturer = forms.ChoiceField(label='Choice', choices= MANUFACTURER_CHOICES)
