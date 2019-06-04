from django.contrib import admin

# Register your models here.
from .models import Customer,Contact

class ContactItemInline(admin.TabularInline):
    model = Contact
    fields = ['name','position','mobile','telephone','email']
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description','address','delivery_address','tax']
    list_filter 		= []
    list_display 		= ('name','description','address','tax')
    readonly_fields 	= ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description']}),
        ('Tax Information',{'fields': ['tax']}),
        ('Address Information',{'fields': ['address','delivery_address']}),
    ]
    inlines = [ContactItemInline]
admin.site.register(Customer,CustomerAdmin)