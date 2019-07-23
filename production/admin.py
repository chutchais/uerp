from django.contrib import admin

# Register your models here.
from .models import Production,RawMaterialUsage,ProductionHour,ScrapHour,WasteHour,DowntimeHour
from recipe.models import RecipeItem
from scrap.models import Scrap
from waste.models import Waste
from downtime.models import Downtime


class ScrapHourAdmin(admin.ModelAdmin):
    list_display        = ['productionhour','scrap','qty','note']
    list_filter         = ['scrap']
    date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['productionhour','scrap','qty','note']}),
    ]
admin.site.register(ScrapHour,ScrapHourAdmin)


class ScrapHourInline(admin.TabularInline):
    model = ScrapHour
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']
    fields = ['scrap','qty','note']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "scrap":
            productionhour = self.get_object(request,ProductionHour)
            if productionhour :
                kwargs["queryset"] = Scrap.objects.filter(productgroup=productionhour.production.job.product.group).order_by('name')
                # print(productionhour)
            # kwargs["queryset"] = Scrap.objects.filter(productgroup=self.production.job.product.productgroup)
        return super(ScrapHourInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_object(self, request, model):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'add':
            return None
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
        print (object_id)
        return model.objects.get(pk=object_id)

class WasteHourAdmin(admin.ModelAdmin):
    list_display        = ['productionhour','waste','qty','note']
    list_filter         = ['waste']
    date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['productionhour','waste','qty','note']}),
    ]
admin.site.register(WasteHour,WasteHourAdmin)


class WasteHourInline(admin.TabularInline):
    model = WasteHour
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']
    fields = ['waste','qty','note']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "waste":
            productionhour = self.get_object(request,ProductionHour)
            if productionhour :
                kwargs["queryset"] = Waste.objects.filter(productgroup=productionhour.production.job.product.group).order_by('name')

        return super(WasteHourInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_object(self, request, model):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'add':
            return None
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
        # print (object_id)
        return model.objects.get(pk=object_id)


class DowntimeHourAdmin(admin.ModelAdmin):
    list_display        = ['productionhour','downtime','start','stop','usage_time','scrap_weight','waste_weight','created_date']
    list_filter         = ['downtime']
    date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['productionhour','downtime','start','stop','usage_time','scrap_weight','waste_weight','note']}),
    ]
admin.site.register(DowntimeHour,DowntimeHourAdmin)

class DowntimeHourInline(admin.TabularInline):
    model = DowntimeHour
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']
    fields = ['downtime','start','stop','usage_time','scrap_weight','waste_weight','note']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "downtime":
            productionhour = self.get_object(request,ProductionHour)
            if productionhour :
                kwargs["queryset"] = Downtime.objects.filter(productgroup=productionhour.production.job.product.group).order_by('name')

        return super(DowntimeHourInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_object(self, request, model):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] == 'add':
            return None
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-2]
        # print (object_id)
        return model.objects.get(pk=object_id)


class RawMaterialUsageInline(admin.TabularInline):
    model = RawMaterialUsage
    readonly_fields=['created_date']
    # autocomplete_fields = ['recipeitem']
    fields = ['recipeitem','lot','planed','actual','note','active']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recipeitem":
            production = self.get_object(request,Production)
            # print ('Master Job %s' % production.job.recipe)
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
    list_filter         = ['production__job__product__group','production__machine']
    list_display        = ['production','hour','line','product_code','weight_roll','roll_min','qty','note']
    date_hierarchy      = 'created_date'
    fieldsets = [
        ('Basic Information',{'fields': ['production','hour','line','product_code','weight_roll','roll_min','qty','note']}),
    ]
    inlines = [ScrapHourInline,WasteHourInline,DowntimeHourInline]
admin.site.register(ProductionHour,ProductionHourAdmin)

class ProductionAdmin(admin.ModelAdmin):
    search_fields       = ['job__name']
    list_filter         = ['shifts','job__product__group']
    list_display        = ('job','shifts','machine','description','machine','production_date','created_date','active','finished')
    autocomplete_fields = ['job','machine']
    readonly_fields     = ['created_date']
    date_hierarchy      = 'production_date'
    fieldsets = [
        ('Basic Information',{'fields': ['job','shifts','description','machine','created_date','active','finished']}),
        ('Build Information',{'fields': ['production_date','order_qty','stock_qty','final_qty']}),
    ]
    inlines =[RawMaterialUsageInline,ProductionHourInline]

admin.site.register(Production,ProductionAdmin)
