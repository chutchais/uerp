from django.contrib import admin

# Register your models here.
from .models import Machine

class MachineAdmin(admin.ModelAdmin):
    search_fields       = ['name','description']
    list_filter         = ['productgroup']
    list_display        = ('name','description','productgroup','created_date')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','productgroup']}),
    ]
admin.site.register(Machine,MachineAdmin)
