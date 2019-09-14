from django.contrib import admin

# Register your models here.

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from order.models import Order,OrderItem
from po.models	  import Po
from product.models import Product

class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem
        import_id_fields = ('seq','order')
        fields = ('seq','order','po','note','created_date','completed')

class OrderItemAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields       = ['order__name','po__name','note']
    list_filter         = []
    list_display        = ('seq','order','po','note','created_date','completed')
    readonly_fields     = ['created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['seq','order','po','note','created_date','completed']}),
        # ('Purchase Order',{'fields': ['pos']}),
    ]
    resource_class      = OrderItemResource
    
admin.site.register(OrderItem,OrderItemAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields =[]
    readonly_fields 	= ['created_date']
    fields = ['seq','po','note','created_date']
    extra = 0
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "po":
            order = self.get_object(request,Order)
            if order :
                kwargs["queryset"] = Po.objects.filter(product=order.product,).order_by('name')
        return super(OrderItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_object(self, request, model):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'add':
            return None
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
        print ('Key =%s' % object_id)
        return model.objects.get(pk=object_id)


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        import_id_fields = ('name',)
        fields = ('name','description','product','created_date','draft','completed')

class OrderAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields 		= ['name','product__name','product__fg_name','description']
    list_filter 		= ('draft','completed',('product',admin.RelatedOnlyFieldListFilter))
    list_display 		= ('name','description','product','pos','weight','created_date','draft','completed')
    readonly_fields 	= ['slug','weight']
    autocomplete_fields = ['product']
    list_display_links  = ['name','product']
    date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','product','draft','completed']}),
        # ('Purchase Order',{'fields': ['pos']}),
    ]
    inlines = [OrderItemInline]
    resource_class      = OrderResource

admin.site.register(Order,OrderAdmin)