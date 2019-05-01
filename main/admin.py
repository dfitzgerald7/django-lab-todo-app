from django.contrib import admin
from .models import Lab, Todo
# Register your models here.

class LabAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lab)
admin.site.register(Todo)