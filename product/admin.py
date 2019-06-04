from django.contrib import admin

# Register your models here.
from .models import (Product,
                    ProductGroup,
                    ProductColor)

class ProductColorAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','code')
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','code']}),
    ]
admin.site.register(ProductColor,ProductColorAdmin)

class ProductGroupAdmin(admin.ModelAdmin):
    search_fields       = ['name','description']
    list_filter         = []
    list_display        = ('name','description')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description']}),
    ]
admin.site.register(ProductGroup,ProductGroupAdmin)


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name','fg_name','group','prod_type']
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name','description','group__name','fg_name']
    list_filter = ['prod_type','group','color__name']
    list_display = ('name','fg_name','qty','parent','description','group','prod_type','prod_unit','color')
    readonly_fields = ['slug','last_warehouse_date']
    fieldsets = [
        ('Basic Information',{'fields': [('name','prod_type'),'slug','description',('group','color')]}),
        ('Warehouse Information',{'fields': ['qty','last_warehouse_date']}),
        ('Bom Level Information',{'fields': ['parent']}),
        ('Finish Goods Information',{'fields': ['fg_name','customer',('weight','weight_runner','weight_unit'),('prod_unit','unit_per_pack','max_pack')]}),
    ]
    inlines = [ProductInline]
admin.site.register(Product,ProductAdmin)


