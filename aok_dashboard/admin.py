from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Business)
admin.site.register(MenuItem)
admin.site.register(BusinessHour)
admin.site.register(Balance)
admin.site.register(AOKPoint)