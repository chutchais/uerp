from django.contrib import admin

# Register your models here.

from .models import Downtime
class DowntimeAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description']
    list_filter 		= ['downtime_type','productgroup']
    list_display 		= ('name','description','downtime_type','productgroup')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','downtime_type','productgroup']}),
    ]
admin.site.register(Downtime,DowntimeAdmin)
