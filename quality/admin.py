from django.contrib import admin

# Register your models here.
from .models import Inspection
class InspectAdmin(admin.ModelAdmin):
    search_fields = ['job','description']
    list_filter = ['to_warehouse']
    list_display = ('job','description','passed','created_date','to_warehouse','to_date')
    readonly_fields = []
    fieldsets = [
        ('Basic Information',{'fields': ['job','description']}),
        ('Warehouse Information',{'fields': ['to_warehouse','passed','to_date']}),
    ]
    # inlines = [ProductInline]
admin.site.register(Inspection,InspectAdmin)