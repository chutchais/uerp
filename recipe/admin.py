from django.contrib import admin

# Register your models here.
# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import Recipe,RecipeItem
from product.models import Product

class RecipeItemInline(admin.TabularInline):
    model = RecipeItem
    fields = ['seq','product','description','ratio']
    extra = 0
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(prod_type='RAW').order_by('name')
        return super(RecipeItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RecipeResource(resources.ModelResource):
    class Meta:
        model = Recipe
        import_id_fields = ('name',)
        fields = ('name','description','prod_group')

class RecipeAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['product__name','description']
    list_filter = ['prod_group']
    list_display = ('name','description','prod_group','active','count','sum','created_date','modified_date')
    readonly_fields = ['slug','created_date','modified_date']
    fieldsets = [
        ('Basic Information',{'fields': [('name','slug'),'prod_group','description','active','created_date','modified_date']}),
    ]
    inlines = [RecipeItemInline]
    resource_class      = RecipeResource
    save_as = True
    save_as_continue = True
    save_on_top =True

admin.site.register(Recipe,RecipeAdmin)


class RecipeItemResource(resources.ModelResource):
    class Meta:
        model = RecipeItem
        import_id_fields = ('recipe','product')
        fields = ('recipe','seq','product','description','ratio','active')

class RecipeItemAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['recipe__name','description']
    list_filter = []
    list_display = ('recipe','seq','product','description','ratio','active')
    readonly_fields = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['recipe','seq',('product','slug'),'description','ratio','active']}),
    ]
    resource_class      = RecipeItemResource

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(prod_type='RAW').order_by('name')
        return super(RecipeItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
admin.site.register(RecipeItem,RecipeItemAdmin)