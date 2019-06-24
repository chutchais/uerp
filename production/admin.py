from django.contrib import admin

# Register your models here.
from .models import Production,RawMaterialUsage,ProductionHour
from recipe.models import RecipeItem

class RawMaterialUsageInline(admin.TabularInline):
    model = RawMaterialUsage
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']
    fields = ['recipeitem','lot','planed','actual','note','active']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recipeitem":
            production = self.get_object(request,Production)
            if production :
                kwargs["queryset"] = RecipeItem.objects.filter(recipe=production.job.recipe,).order_by('product')
        return super(RawMaterialUsageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_object(self, request, model):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'add':
            return None
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
        print (object_id)
        return model.objects.get(pk=object_id)


class RawMaterialUsageAdmin(admin.ModelAdmin):
    search_fields       = ['recipeitem__product__name','lot']
    list_filter         = ['recipeitem']
    list_display        = ('production','recipeitem','lot','planed','actual','created_date','active')
    autocomplete_fields = ['production','recipeitem']
    readonly_fields     = ['created_date']
    fieldsets = [
        ('Basic Information',{'fields': ['production','recipeitem','lot','planed','actual','note','created_date','active']}),
    ]

admin.site.register(RawMaterialUsage,RawMaterialUsageAdmin)


class ProductionHourInline(admin.TabularInline):
    model = ProductionHour
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']

    fields = ['hour','line','product_code','weight_roll','roll_min','qty','note']
    extra = 0
    show_change_link = True

class ProductionHourAdmin(admin.ModelAdmin):
    list_display        = ['hour','line','product_code','weight_roll','roll_min','qty','note']
    date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['hour','line','product_code','weight_roll','roll_min','qty','note']}),
    ]
admin.site.register(ProductionHour,ProductionHourAdmin)

class ProductionAdmin(admin.ModelAdmin):
    search_fields       = ['job__name']
    list_filter         = ['shifts','job__product__group']
    list_display        = ('job','shifts','machine','description','machine','production_date','created_date','active')
    autocomplete_fields = ['job','machine']
    readonly_fields     = ['created_date']
    date_hierarchy      = 'production_date'
    fieldsets = [
        ('Basic Information',{'fields': ['job','shifts','description','machine','created_date','active']}),
        ('Build Information',{'fields': ['production_date','order_qty','stock_qty','final_qty']}),
    ]
    inlines =[RawMaterialUsageInline,ProductionHourInline]

admin.site.register(Production,ProductionAdmin)
