from django.contrib import admin
from django.forms import ModelForm

# Register your models here.
from .models import Job,Complete,RawMaterialUsage
from machine.models import Machine
from product.models import Product
from recipe.models import RecipeItem


class CompleteInline(admin.TabularInline):
    model = Complete
    readonly_fields=['stamp_date']
    fields = ['description','qty','stamp_date']
    extra = 0

from machine.models import Machine


class RawMaterialUsageInline(admin.TabularInline):
    model = RawMaterialUsage
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']
    fields = ['recipeitem','planed','actual','active']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recipeitem":
            job = self.get_object(request,Job)
            if job :
                kwargs["queryset"] = RecipeItem.objects.filter(recipe=job.recipe,).order_by('product')
        return super(RawMaterialUsageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_object(self, request, model):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'add':
            return None
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
        print (object_id)
        return model.objects.get(pk=object_id)


class RawMaterialUsageAdmin(admin.ModelAdmin):
    search_fields       = ['job','recipeitem']
    list_filter         = ['recipeitem']
    list_display        = ('job','recipeitem','planed','actual','created_date','active')
    autocomplete_fields = ['job','recipeitem']
    readonly_fields     = ['created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['job','recipeitem','planed','actual','created_date','active']}),
    ]

admin.site.register(RawMaterialUsage,RawMaterialUsageAdmin)

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
    inlines =[RawMaterialUsageInline,CompleteInline]
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



