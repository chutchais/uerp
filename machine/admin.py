from django.contrib import admin

# Register your models here.
from .models import Machine

# For Export Data
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

class MachineResource(resources.ModelResource):

	class Meta:
		model = Machine
		import_id_fields = ('name',)
		fields =('name','description','productgroup')


class MachineAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
	search_fields       = ['name','description']
	list_filter         = ['productgroup']
	list_display        = ('name','description','productgroup','created_date')
	readonly_fields     = ['slug','created_date','modified_date','created_user']
	resource_class 		= MachineResource
	fieldsets = [
		('Basic Information',{'fields': ['name','slug','description','productgroup',
										('created_date','created_user'),'modified_date']}),
	]

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'created_user', None) is None:
			obj.created_user = request.user
		obj.save()

admin.site.register(Machine,MachineAdmin)
