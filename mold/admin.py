from django.contrib import admin

# Register your models here.
# from .models import Machine,MachineCapacity
from .models import Mold,MoldCapacity

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin


class MoldCapacityInline(admin.TabularInline):
    model = MoldCapacity
    fields = ['machine','output','shot_per_day','piece_per_day']
    readonly_fields     = ['shot_per_day','piece_per_day']
    autocomplete_fields = ['machine']
    extra = 0
    verbose_name = 'Mold Capacity'
    verbose_name_plural = 'Mold Capacities'

class MoldResource(resources.ModelResource):

	class Meta:
		model = Mold
		import_id_fields = ('name',)
		skip_unchanged = True
		report_skipped= True
		fields =('name','description','productgroup','brand','max_cap')

# class MachineshipInline(admin.TabularInline):
#     model = Mold.machines.through
#     extra = 0

class MoldAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
	search_fields       = ['name','description','brand']
	list_filter         = []
	list_display        = ('name','brand','product','standard_weight','cavity','available','weight',)
	readonly_fields     = ['slug','created_date','modified_date','created_user','weight','runner',
						'product_weight_g','product_weight_kg','weight_total','weight_yield']
	resource_class 		= MoldResource
	fieldsets = [
		('Basic Information',{'fields': ['name','brand','description',
										('product','weight','runner','product_weight_g','product_weight_kg'),
										('standard_weight','cavity','available','weight_total'),
										('weight_yield'),
										('created_date','created_user'),'modified_date']}),
	]
	autocomplete_fields = ['product']
	inlines = [MoldCapacityInline]
	save_as = True
	save_as_continue = True
	save_on_top =True

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'created_user', None) is None:
			obj.created_user = request.user
		obj.save()

admin.site.register(Mold,MoldAdmin)





