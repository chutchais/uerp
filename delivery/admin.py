from django.contrib import admin

# Register your models here.
from .models import Delivery

class DeliveryAdmin(admin.ModelAdmin):
    search_fields 		= ['invoice','description','po__name']
    list_filter 		= []
    list_display 		= ('invoice','po','description','qty','delivery_date','delivery_address')
    readonly_fields 	= []
    autocomplete_fields = ['po']
    fieldsets = [
        ('Basic Information',{'fields': ['invoice','po','description']}),
        ('Delivery Information',{'fields': ['qty','delivery_date','delivery_address']}),
    ]

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'product':
    #         kwargs["queryset"] = Product.objects.filter(prod_type = 'FG').order_by('name')
    #         # print ('prodyuct......................')
    #     return super(PoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # inlines = [JobInline]
admin.site.register(Delivery,DeliveryAdmin)
