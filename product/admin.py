from django.contrib import admin

# Register your models here.
from .models import (Product,
                    ProductGroup,
                    ProductColor,ProductBrand)

admin.site.register(ProductBrand)

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
    verbose_name = 'SEMI Part'
    verbose_name_plural = 'SEMI Parts'

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name','description','group__name','fg_name']
    list_filter = ['prod_type','group','brand','color__name']
    list_display = ('name','fg_name','qty','parent','description','brand','group','prod_type','prod_unit','color')
    readonly_fields = ['slug','last_warehouse_date']
    autocomplete_fields = ['parent']
    ordering = ['name']
    fieldsets = [
        ('Basic Information',{'fields': [('name','prod_type'),'slug','description',('group','color')]}),
        ('Brand',{'fields': ['brand']}),
        ('Warehouse Information',{'fields': [('qty','last_warehouse_date'),'min_order']}),
        ('Job Prefix Information',{'fields': ['job_prefix']}),
        ('Bom Level Information',{'fields': ['parent']}),
        ('Finish Goods Information',{'fields': ['fg_name','customer',('weight','weight_runner','weight_unit'),('prod_unit','unit_per_pack','max_pack')]}),
    ]
    inlines = [ProductInline]
admin.site.register(Product,ProductAdmin)


