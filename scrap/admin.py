from django.contrib import admin

# Register your models here.
from .models import Scrap
class ScrapAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description']
    list_filter 		= ['productgroup']
    list_display 		= ('name','description','productgroup')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','productgroup']}),
    ]
admin.site.register(Scrap,ScrapAdmin)
