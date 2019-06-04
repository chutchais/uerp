from django.contrib import admin

# Register your models here.
from order.models import Order,OrderItem
from po.models	  import Po


class OrderItemAdmin(admin.ModelAdmin):
    search_fields       = ['order__name','po__name','note']
    list_filter         = []
    list_display        = ('seq','order','po','note','created_date','completed')
    readonly_fields     = ['created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['seq','order','po','note','created_date','completed']}),
        # ('Purchase Order',{'fields': ['pos']}),
    ]
admin.site.register(OrderItem,OrderItemAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields =[]
    readonly_fields 	= ['created_date']
    fields = ['seq','po','note','created_date']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    search_fields 		= ['name','product__name','product__fg_name','description']
    list_filter 		= ['draft','completed','product']
    list_display 		= ('name','description','product','pos','weight','created_date','draft','completed')
    readonly_fields 	= ['slug','weight']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','product','draft','completed']}),
        # ('Purchase Order',{'fields': ['pos']}),
    ]
    inlines = [OrderItemInline]
admin.site.register(Order,OrderAdmin)