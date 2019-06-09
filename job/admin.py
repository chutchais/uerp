from django.contrib import admin

# Register your models here.
from .models import Job,Complete

class CompleteInline(admin.TabularInline):
    model = Complete
    readonly_fields=['stamp_date']
    fields = ['description','qty','stamp_date']
    extra = 0


class JobAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description','product__name','order__name']
    list_filter 		= ['finished','qc_checked','product__name']
    list_display 		= ('name','description','product','qty','start_date','stop_date','completed',
                            'balance','finished','qc_checked','passed','active')
    readonly_fields 	= ['slug','completed','balance','finished_date']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','product','active']}),
        ('Build Order',{'fields': [('order')]}),
        ('Recipe',{'fields': ['recipe']}),
        
        ('Plan Schedule',{'fields': [('qty','completed','balance'),('start_date','stop_date')]}),
        ('Job Finished',{'fields': ['finished','finished_date']}),
    ]
    inlines =[CompleteInline]
admin.site.register(Job,JobAdmin)