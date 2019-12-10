from django.contrib import admin

# Register your models here.
from .models import (Product,
                    ProductGroup,
                    ProductColor,ProductBrand)

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped= True
        fields =('name','fg_name','description','parent','group','customer','brand',
                'prod_type','prod_unit','color',
                'weight','weight_runner','weight_unit','qty')


class ProductBrandResource(resources.ModelResource):
    class Meta:
        model = ProductBrand
        import_id_fields = ('name',)
        fields = ('name','description')

class ProductBrandAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','created_date')
    fieldsets = [
        ('Basic Information',{'fields': ['name','description']}),
    ]
    resource_class      = ProductBrandResource
    save_as = True
    save_as_continue = True
    save_on_top =True

admin.site.register(ProductBrand,ProductBrandAdmin)


class ProductColorResource(resources.ModelResource):
    class Meta:
        model = ProductColor
        import_id_fields = ('name',)
        fields = ('name','description')

class ProductColorAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','code')
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','code']}),
    ]
    resource_class      = ProductColorResource
    save_as = True
    save_as_continue = True
    save_on_top =True
    
admin.site.register(ProductColor,ProductColorAdmin)

class ProductGroupResource(resources.ModelResource):
    class Meta:
        model = ProductGroup
        import_id_fields = ('name',)
        fields = ('name','description')

class ProductGroupAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields       = ['name','description']
    list_filter         = []
    list_display        = ('name','description')
    readonly_fields     = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description']}),
    ]
    resource_class      = ProductGroupResource
    save_as = True
    save_as_continue = True
    save_on_top =True

admin.site.register(ProductGroup,ProductGroupAdmin)


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name','fg_name','group','prod_type']
    extra = 0
    verbose_name = 'SEMI Part'
    verbose_name_plural = 'SEMI Parts'

class ProductAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name','description','group__name','fg_name']
    list_filter = ('prod_type',('group',admin.RelatedOnlyFieldListFilter),'brand','color__name')
    list_display = ('name','fg_name','qty','parent','description','brand','group','prod_type','prod_unit','color')
    readonly_fields = ['slug','last_warehouse_date']
    autocomplete_fields = ['parent']
    ordering = ['name']
    list_display_links  = ['name','parent']
    fieldsets = [
        ('Basic Information',{'fields': [('name','prod_type'),'slug',('fg_name','customer'),'description',('group','color')]}),
        ('Brand',{'fields': ['brand']}),
        ('Warehouse Information',{'fields': [('qty','last_warehouse_date'),'min_order']}),
        ('Job Prefix Information',{'fields': ['job_prefix']}),
        ('Bom Level Information',{'fields': ['parent']}),
        ('Finish Goods Information',{'fields': [('weight','weight_runner','weight_unit'),('prod_unit','unit_per_pack','max_pack')]}),
    ]
    inlines = [ProductInline]
    resource_class      = ProductResource
    save_as = True
    save_as_continue = True
    save_on_top =True

admin.site.register(Product,ProductAdmin)


