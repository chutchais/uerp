from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Sum

# Create your models here.
from product.models import Product,ProductGroup

class Recipe(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	prod_group		= models.ForeignKey(ProductGroup, null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='recipes')
	description 	= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)


	def __str__(self):
		return ('%s' % (self.name))

	def count(self):
		return self.items.count()

	def sum(self):
		return round(self.items.aggregate(Sum('ratio'))['ratio__sum'],3)

	def get_absolute_url(self):
		return reverse('recipe:detail', kwargs={'slug': self.slug})

def pre_save_recipe_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_recipe_receiver, sender=Recipe)


class RecipeItem(models.Model):
	# name 			= models.CharField(max_length=50,null = False)
	description 	= models.CharField(max_length=100,null = True,blank = True)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	recipe 			= models.ForeignKey(Recipe, null=True,blank = True,
							on_delete=models.CASCADE,
							related_name='items')
	seq				= models.IntegerField(default=1)
	product			= models.ForeignKey(Product,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'recipeintems')
	ratio			= models.DecimalField(default=0,max_digits=8, decimal_places=3)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)


	def __str__(self):
		return ('%s' % self.product)

def pre_save_recipeitem_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify('%s-%s' % (instance.recipe.name,instance.product))

pre_save.connect(pre_save_recipeitem_receiver, sender=RecipeItem)