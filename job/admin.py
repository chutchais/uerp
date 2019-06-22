from django.contrib import admin
from django.forms import ModelForm

# Register your models here.
from .models import Job,Complete
from machine.models import Machine
from product.models import Product

class CompleteInline(admin.TabularInline):
    model = Complete
    readonly_fields=['stamp_date']
    fields = ['description','qty','stamp_date']
    extra = 0

from machine.models import Machine

class JobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # self.instance = kwargs.pop('instance', None)
        super(JobForm, self).__init__(*args, **kwargs)
        # if self.instance.product :
        #     self.fields['machine'].queryset = Machine.objects.filter(productgroup = self.instance.product.group)

class JobAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description','product__name','order__name']
    list_filter 		= ('finished','qc_checked',('product',admin.RelatedOnlyFieldListFilter))
    list_display 		= ('name','order','product','qty','start_date','stop_date','completed',
                            'balance','finished','qc_checked','passed','active')
    readonly_fields 	= ['slug','completed','balance','finished_date']
    autocomplete_fields = ['machine']
    list_display_links  = ['name','order','product']
    date_hierarchy      = 'created_date'
    # save_on_top         = True
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','product','active']}),
        ('Build Order',{'fields': [('order')]}),
        ('Recipe',{'fields': ['recipe']}),
        ('Machine',{'fields': ['machine']}),
        ('Plan Schedule',{'fields': [('qty','completed','balance'),('start_date','stop_date')]}),
        ('Job Finished',{'fields': ['finished','finished_date']}),
    ]
    inlines =[CompleteInline]
    form = JobForm

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'machine':
    #         # job = self.get_object(request,Job)
    #         print(request)
    #         if None :
    #             kwargs["queryset"] = Machine.objects.filter(productgroup = product.group).order_by('name')
    #         # print ('prodyuct......................')
    #     return super(JobAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Job,JobAdmin)