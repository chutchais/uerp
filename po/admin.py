from django.contrib import admin

# Register your models here.
from .models import Po
from job.models import Job

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


class PoAdmin(admin.ModelAdmin):
    search_fields 		= ['name','description','product__name']
    list_filter 		= ['started','completed','product']
    list_display 		= ('name','order','product','qty','weight','weight_unit','delivery_date','started','completed','active')
    readonly_fields 	= ['slug','order','weight','weight_unit']
    fieldsets = [
        ('Basic Information',{'fields': ['name','slug','description','started','completed','active']}),
        ('Purchasing Information',{'fields': ['customer',('product','qty','weight','weight_unit'),'delivery_date','delivery_address']}),
        ('Build Order Information',{'fields': ['order']}),
    ]
    # inlines = [JobInline]
admin.site.register(Po,PoAdmin)