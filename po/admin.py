from django.contrib import admin

# Register your models here.
from .models import Po
from job.models import Job
from product.models import Product

# class FaqForm(forms.ModelForm):
# 	description = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
# 	class Meta:
# 		model = Job
# 		fields = ('__all__')

# class JobInline(admin.TabularInline):
#     model = Job
#     readonly_fields =['completed']
#     fields = ['name','product','qty','start_date','stop_date','completed']
#     extra = 0

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

class PoResource(resources.ModelResource):
    class Meta:
        model = Po
        import_id_fields = ('name',)
        fields = ('name','description','po_type','product','order',
            'qty','weight','weight_unit','delivery_date','delivery_address',
            'started','completed','active')

class PoAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields 		= ['name','description','product__name']
    list_filter 		= ['started','completed','po_type','product__group']
    list_display 		= ('name','order','product','qty','weight','weight_unit','delivery_date','started','completed','active')
    readonly_fields 	= ['slug','order','weight','weight_unit']
    autocomplete_fields = ['product','customer']
    list_display_links  = ['name','order','product']
    # date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','po_type','description','started','completed','active']}),
        ('Purchasing Information',{'fields': ['customer',('product','qty','weight','weight_unit'),'delivery_date','delivery_address']}),
        ('Build Order Information',{'fields': ['order']}),
    ]
    resource_class      = PoResource
    save_as = True
    save_as_continue = True
    save_on_top =True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs["queryset"] = Product.objects.filter(prod_type = 'FG').order_by('name')
            # print ('prodyuct......................')
        return super(PoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # inlines = [JobInline]
admin.site.register(Po,PoAdmin)