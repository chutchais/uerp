from django.contrib import admin

# Register your models here.
from .models import Recipe,RecipeItem

class RecipeItemInline(admin.TabularInline):
    model = RecipeItem
    fields = ['seq','product','description','ratio']
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['product__name','description']
    list_filter = ['prod_group']
    list_display = ('name','description','prod_group','active','count','sum','created_date','modified_date')
    readonly_fields = ['slug','created_date','modified_date']
    fieldsets = [
        ('Basic Information',{'fields': [('name','slug'),'prod_group','description','active','created_date','modified_date']}),
    ]
    inlines = [RecipeItemInline]
admin.site.register(Recipe,RecipeAdmin)


class RecipeItemAdmin(admin.ModelAdmin):
    search_fields = ['description']
    list_filter = []
    list_display = ('recipe','seq','product','description','ratio','active')
    readonly_fields = ['slug']
    fieldsets = [
        ('Basic Information',{'fields': ['recipe','seq',('product','slug'),'description','ratio','active']}),
    ]
admin.site.register(RecipeItem,RecipeItemAdmin)