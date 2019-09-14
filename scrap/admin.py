from django.contrib import admin

# Register your models here.

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import Scrap

class ScrapResource(resources.ModelResource):
    class Meta:
        model = Scrap
        import_id_fields = ('name',)
        fields = ('name','description','productgroup')

class ScrapAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields 		= ['name','description']
    list_filter 		= ['productgroup']
    list_display 		= ('name','description','productgroup')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','productgroup']}),
    ]
    resource_class      = ScrapResource
    save_as = True
    save_as_continue = True
    save_on_top =True
admin.site.register(Scrap,ScrapAdmin)
