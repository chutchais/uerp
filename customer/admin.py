from django.contrib import admin

# Register your models here.
from .models import Customer,Contact

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped= True
        fields =('name','description','address','delivery_address','tax')

class ContactItemInline(admin.TabularInline):
    model = Contact
    fields = ['name','position','mobile','telephone','email']
    extra = 0

class CustomerAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    search_fields 		= ['name','description','address','delivery_address','tax']
    list_filter 		= []
    list_display 		= ('name','description','address','tax')
    readonly_fields     = ['slug','created_date','created_user','modified_date']  
    resource_class      = CustomerResource
    save_as             = True
    save_as_continue    = True
    save_on_top         = True

    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description']}),
        ('Tax Information',{'fields': ['tax']}),
        ('Address Information',{'fields': ['address','delivery_address']}),
        ('System Information',{'fields': ['created_date','created_user','modified_date']})
    ]
    inlines = [ContactItemInline]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_user', None) is None:
            obj.created_user = request.user
        obj.save()

admin.site.register(Customer,CustomerAdmin)