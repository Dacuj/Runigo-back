from django.contrib import admin
from .models import University, Mentors, Comments 
# Register your models here.
admin.site.register(Mentors)
admin.site.register(Comments)
admin.site.register(University)
