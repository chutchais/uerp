from django.contrib import admin

# Register your models here.
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

class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['product__name','description']
    list_filter = ['prod_group']
    list_display = ('name','description','prod_group','active','count','sum','created_date','modified_date')
    readonly_fields = ['slug','created_date','modified_date']
    fieldsets = [
        ('Basic Information',{'fields': [('name','slug'),'prod_group','description','active','created_date','modified_date']}),
    ]
    inlines = [RecipeItemInline]


admin.site.register(Recipe,RecipeAdmin)


class RecipeItemAdmin(admin.ModelAdmin):
    search_fields = ['description']
    list_filter = []
    list_display = ('recipe','seq','product','description','ratio','active')
    readonly_fields = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['recipe','seq',('product','slug'),'description','ratio','active']}),
    ]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(prod_type='RAW').order_by('name')
        return super(RecipeItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
admin.site.register(RecipeItem,RecipeItemAdmin)