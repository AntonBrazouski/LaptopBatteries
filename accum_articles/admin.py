from django.contrib import admin

from accum_articles.models import LaptopBattery, BatteryDescription
# Register your models here.

admin.site.register([LaptopBattery, BatteryDescription])
