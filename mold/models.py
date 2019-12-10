from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Sum
from django.contrib.auth.models import User
from product.models import Product,ProductGroup
from machine.models import Machine
# Create your models here.
class Mold(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	brand 			= models.CharField(max_length=20,null = True,blank = True)
	cavity	 		= models.IntegerField(verbose_name='Cavity',default=1)
	available 		= models.IntegerField(verbose_name='Available Used',default=1)
	standard_weight	= models.DecimalField(verbose_name='Standard weight(g)',default=1,
					max_digits=7, decimal_places=2)

	product			= models.ForeignKey(Product,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'molds')
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	draft			= models.BooleanField(default=True)
	active			= models.BooleanField(default=True)
	created_user	= models.ForeignKey(User, on_delete=models.SET_NULL,
						blank=True,null=True)

	@property
	def weight(self):
		c = self.product.weight 
		return c
	weight.fget.short_description = "Product Weight(g)"

	@property
	def runner(self):
		c = self.product.weight_runner
		return c
	runner.fget.short_description = "Runner Weight(g)"

	@property
	def product_weight_g(self):
		c = self.weight + self.runner
		return c
	product_weight_g.fget.short_description = "Product Weight(g)"

	@property
	def product_weight_kg(self):
		c = int((self.unit_weight_g)/1000)
		return c
	product_weight_kg.fget.short_description = "Product Weight(Kg)"

	@property
	def weight_total(self):
		c = self.product.weight * self.available
		return c
	weight_total.fget.short_description = "Total Unit Weight(g)"

	@property
	def weight_yield(self):
		c = int((self.weight_total / self.product_weight_g)*100)
		return c
	weight_yield.fget.short_description = "Yield (%)"

	class Meta:
		verbose_name = 'Mold'
		verbose_name_plural = 'Molds'

	def __str__(self):
		return ('%s' % self.name)

	def get_absolute_url(self):
		return reverse('mold:detail', kwargs={'slug': self.slug})

def create_mold_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Mold.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.count())
		return create_mold_slug(instance, new_slug=new_slug)
	return slug

def pre_save_mold_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_mold_slug(instance)

pre_save.connect(pre_save_mold_receiver, sender=Mold)



class MoldCapacity(models.Model):
	mold 				= models.ForeignKey(Mold, on_delete=models.CASCADE,related_name = 'mold_capacities')
	machine 			= models.ForeignKey(Machine, on_delete=models.CASCADE,related_name = 'mold_capacities')
	output 				= models.IntegerField(verbose_name='Output/Day (Kgs)',default=0)
	modified_date		= models.DateTimeField(blank=True, null=True,auto_now=True)

	@property
	def shot_per_day(self):
		c = (self.output*1000) / self.mold.product_weight_g
		return int(c)
	shot_per_day.fget.short_description = "Shot/Day"

	@property
	def piece_per_day(self):
		c = (self.shot_per_day) * self.mold.cavity
		return int(c)
	piece_per_day.fget.short_description = "Output Piece/Day"