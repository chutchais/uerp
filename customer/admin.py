from django.contrib import admin

# Register your models here.
from .models import Customer
class CustomerAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description']
    list_filter 		= []
    list_display 		= ('name','description')
    readonly_fields 	= ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description']}),
        ('Address Information',{'fields': ['address','delivery_address']}),
    ]
admin.site.register(Customer,CustomerAdmin)