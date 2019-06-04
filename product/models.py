from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone

# Create your models here.
from customer.models import Customer

class ProductGroup(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)


	def __str__(self):
		return ('%s (%s)' % (self.name,self.description))

def create_productgroup_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = ProductGroup.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_productgroup_slug(instance, new_slug=new_slug)
    return slug

def pre_save_productgroup_receiver(sender, instance, *args, **kwargs):
    
    if not instance.slug:
        instance.slug = create_productgroup_slug(instance)

pre_save.connect(pre_save_productgroup_receiver, sender=ProductGroup)

class ProductColor(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	description 	= models.TextField(null = True,blank = True)
	code			= models.CharField(max_length=20,null = False,default='#FFFFFF')
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)


	def __str__(self):
		return ('%s (%s)' % (self.name,self.description))



# Product Type
CONSUMABLE		= 	'CON'
FINISH_GOOD		=	'FG'
SEMI			=	'SEMI'
RAW_MATERIAL	= 	'RAW'
SET 			=	'SET'
OTHER			=	'OT'
PRODUCT_TYPE_CHOICES = (
		(CONSUMABLE, 'Consumable'),
		(FINISH_GOOD, 'Finish Goods'),
		(SEMI,'Semi part'),
		(SET,'Sets'),
		(RAW_MATERIAL,'Raw Material'),
		(OTHER,'Other')
	)

# Product Unit
# Box,Pice,Roll,Section
BOX 		= 'BOX'
PICE 		= 'PICE'
ROLL 		= 'ROLL'
SECTION 	= 'SECTION'
OTHER 		= 'OTHER'
PRODUCT_UNIT_CHOICES = (
		(BOX,'Box'),
		(PICE,'Pice'),
		(ROLL,'Roll'),
		(SECTION,'Section'),
		(OTHER,'Other')
	)

GRAM		=	'GRAM'
KILO		=	'KILO'
PRODUCT_WEIGHT_UNIT = (
		(GRAM,'Gram'),
		(KILO,'Kilogram')
	)


class Product(models.Model):
	name 				= models.CharField(primary_key=True,max_length=50,null = False)
	fg_name				= models.CharField(verbose_name='Finish Goods Name',max_length=50,blank=True, null=True)
	slug 				= models.SlugField(unique=True,blank=True, null=True)
	description 		= models.TextField(null = True,blank = True)
	parent 				= models.ForeignKey('self', null=True,blank = True,
							on_delete=models.SET_NULL,
							related_name='products')
	group				= models.ForeignKey(ProductGroup,
							blank=True,null=True,
							on_delete = models.SET_NULL,
							related_name = 'products')
	customer			= models.ForeignKey(Customer,
							blank=True,null=True,
							on_delete = models.SET_NULL,
							related_name = 'products')
	prod_type			= models.CharField(max_length=5,choices=PRODUCT_TYPE_CHOICES,default=RAW_MATERIAL)
	prod_unit			= models.CharField(max_length=10,choices=PRODUCT_UNIT_CHOICES,default=PICE)
	color 				= models.ForeignKey(ProductColor,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'products')
	max_pack			= models.IntegerField(verbose_name='Pack per box',default=1)
	unit_per_pack		= models.DecimalField(verbose_name='Unit per pack',default=1,max_digits=7, decimal_places=2)
	weight				= models.DecimalField(verbose_name='Unit weight',default=0,max_digits=7, decimal_places=2)#Only Finish good weight
	weight_runner		= models.DecimalField(verbose_name='Runner weight',default=0,max_digits=7, decimal_places=2)#Only Runner weight
	weight_unit 		= models.CharField(verbose_name='Weight unit',max_length=10,choices=PRODUCT_WEIGHT_UNIT,default=GRAM)
	created_date		= models.DateTimeField(auto_now_add=True)
	modified_date		= models.DateTimeField(blank=True, null=True,auto_now=True)
	active				= models.BooleanField(default=True)
	# warehouse control
	qty					= models.IntegerField(verbose_name='On Warehouse',default=0)
	last_warehouse_date	= models.DateTimeField(blank=True, null=True)



	def __str__(self):
		return ('%s (%s)' % (self.name,self.description))

	def weight_pending_build(self):
		return 0

	def weight_on_building(self):
		return 0

	def weight_total(self):
		return self.weight+self.weight_runner

	def get_absolute_url(self):
		return reverse('product:detail', kwargs={'slug': self.slug})

	def increase_qty(self,qty):
		self.qty 					= self.qty + qty
		self.last_warehouse_date 	= timezone.now()
		self.save()
		return self.qty

	def decrease_qty(self,qty):
		self.qty 					= self.qty - qty
		self.last_warehouse_date 	= timezone.now()
		self.save()
		return self.qty

# def create_product_slug(instance, new_slug=None):
#     slug = slugify(instance.name)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Vessel.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug, qs.first().lov)
#         return create_vessel_slug(instance, new_slug=new_slug)
#     return slug

def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_product_receiver, sender=Product)