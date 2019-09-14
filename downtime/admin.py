from django.contrib import admin

# Register your models here.

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import Downtime

class DowntimeResource(resources.ModelResource):
    class Meta:
        model = Downtime
        import_id_fields = ('name',)
        fields = ('name','description','downtime_type','productgroup')

class DowntimeAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields 		= ['name','description']
    list_filter 		= ['downtime_type','productgroup']
    list_display 		= ('name','description','downtime_type','productgroup')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','downtime_type','productgroup']}),
    ]
    resource_class      = DowntimeResource
    save_as = True
    save_as_continue = True
    save_on_top =True
    
admin.site.register(Downtime,DowntimeAdmin)
