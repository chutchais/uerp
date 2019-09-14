from django.contrib import admin

# Register your models here.
# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import Inspection

class InspectionResource(resources.ModelResource):
    class Meta:
        model = Inspection
        import_id_fields = ('job','description')
        fields = ('job','description','passed','created_date','to_warehouse','to_date')

class InspectAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['job','description']
    list_filter = ['to_warehouse']
    list_display = ('job','description','passed','created_date','to_warehouse','to_date')
    readonly_fields = []
    fieldsets = [
        ('Basic Information',{'fields': ['job','description']}),
        ('Warehouse Information',{'fields': ['to_warehouse','passed','to_date']}),
    ]
    resource_class      = InspectionResource
    # inlines = [ProductInline]
admin.site.register(Inspection,InspectAdmin)