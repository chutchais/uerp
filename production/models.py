from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone

# Create your models here.

# Master
from job.models import Job
from machine.models import Machine


M		=	'MORNING'
N		=	'NIGHT'
SHIFTS_TYPE_CHOICE = (
		(M,'Morning'),
		(N,'Night')
	)

class Production(models.Model):
	description 	= models.TextField(null = True,blank = True)
	job 			= models.ForeignKey(Job,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'productions')
	shifts 			= models.CharField(max_length=20,choices=SHIFTS_TYPE_CHOICE,default=M)
	machine			= models.ForeignKey(Machine,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'productions')
	production_date	= models.DateField(blank=True, null=True)
	order_qty 		= models.IntegerField(default=0)
	stock_qty 		= models.IntegerField(default=0)
	final_qty 		= models.IntegerField(default=0)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	class Meta:
		unique_together = [['job', 'shifts']]

	def __str__(self):
		return ('%s on %s' % (self.job,self.shifts))

	def get_absolute_url(self):
		return reverse('production:detail', kwargs={'pk': self.pk})
# Detail
S1 = 1
S2 = 2
S3 = 3
S4 = 4
S5 = 5
S6 = 6
S7 = 7
S8 = 8
S9 = 9
S10 =10
S11 = 11
S12 = 12
S13 = 13
S14 = 14
S15 = 15
S16 = 16
S17 = 17
S18 = 18
S19 = 19
S20 = 20
S21 = 21
S22 = 22
S23 = 23
S24 = 24
HOUR_TYPE_CHOICE = (
		(S1,'00-01'),
		(S2,'01-02'),
		(S3,'02-03'),
		(S4,'03-04'),
		(S5,'04-05'),
		(S6,'05-06'),
		(S7,'06-07'),
		(S8,'07-08'),
		(S9,'08-09'),
		(S10,'09-10'),
		(S11,'10-11'),
		(S12,'11-12'),
		(S13,'12-13'),
		(S14,'13-14'),
		(S15,'14-15'),
		(S16,'15-16'),
		(S17,'16-17'),
		(S18,'17-18'),
		(S19,'18-19'),
		(S20,'19-20'),
		(S21,'20-21'),
		(S22,'21-22'),
		(S23,'22-23'),
		(S24,'23-00'),
	)
LINE_TYPE_CHOICE = (
		(1,1),
		(2,2),
		(3,3),
		(4,4)
)

class ProductionHour(models.Model):
	production		= models.ForeignKey(Production,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'hours')
	hour 			= models.IntegerField(choices=HOUR_TYPE_CHOICE,default=7)
	line 			= models.IntegerField(choices=LINE_TYPE_CHOICE,default=1)
	product_code	= models.CharField(max_length=50,blank=True, null=True)
	weight_roll		= models.DecimalField(verbose_name='Weight per roll',default=1,max_digits=7, decimal_places=2)
	roll_min		= models.DecimalField(verbose_name='Roll per min',default=1,max_digits=7, decimal_places=2)
	qty 			= models.IntegerField(default=1)
	note 			= models.CharField(max_length=100,null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s on %s' % (self.production,self.hour))

	def get_absolute_url(self):
		return reverse('production:hour', kwargs={'pk': self.pk})

# Scrap per Hour
from scrap.models import Scrap
class ScrapHour(models.Model):
	productionhour 	= models.ForeignKey(ProductionHour,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'scraps')
	scrap 			= models.ForeignKey(Scrap,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'scraps')
	qty				= models.DecimalField(verbose_name='Scrap Qty',default=1,max_digits=7, decimal_places=2)
	note 			= models.CharField(max_length=100,null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % (self.scrap)) 

# Scrap per Hour
from waste.models import Waste
class WasteHour(models.Model):
	productionhour 	= models.ForeignKey(ProductionHour,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'wastes')
	waste 			= models.ForeignKey(Waste,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'wastes')
	qty				= models.DecimalField(verbose_name='Waste Qty',default=1,max_digits=7, decimal_places=2)
	note 			= models.CharField(max_length=100,null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % (self.waste)) 

# Downtime per Hour
from downtime.models import Downtime
class DowntimeHour(models.Model):
	productionhour 	= models.ForeignKey(ProductionHour,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'downtimes')
	downtime 		= models.ForeignKey(Downtime,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'downtimes')
	start			= models.TimeField(blank=True, null=True)
	stop			= models.TimeField(blank=True, null=True)
	usage_time		= models.DecimalField(verbose_name='Usage time (min)',default=0,max_digits=7, decimal_places=2)
	scrap_weight 	= models.DecimalField(verbose_name='Scrap weight',default=0,max_digits=7, decimal_places=2)
	waste_weight  	= models.DecimalField(verbose_name='Waste weight',default=0,max_digits=7, decimal_places=2)
	note 			= models.CharField(max_length=100,null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % (self.downtime)) 



from recipe.models import RecipeItem
class RawMaterialUsage(models.Model):
	production			= models.ForeignKey(Production,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'rawusages')
	recipeitem		= models.ForeignKey(RecipeItem,
							null = True,blank = True,
							on_delete=models.SET_NULL,
							related_name = 'rawusages')
	planed			= models.DecimalField(default=0,max_digits=8, decimal_places=3)
	actual			= models.DecimalField(default=0,max_digits=8, decimal_places=3)
	lot 			= models.CharField(max_length=50,null = True,blank = True)
	note 			= models.CharField(max_length=100,null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % (self.recipeitem))




# class Po(models.Model):
# 	name 			= models.CharField(primary_key=True,max_length=50,null = False)
# 	slug 			= models.SlugField(unique=True,blank=True, null=True)
# 	description 	= models.TextField(null = True,blank = True)
# 	qty				= models.IntegerField(default=0)
# 	customer		= models.ForeignKey(Customer,
# 							blank=True,null=True,
# 							on_delete=models.SET_NULL,
# 							related_name = 'pos')
# 	product			= models.ForeignKey(Product,
# 							blank=True,null=True,
# 							on_delete=models.SET_NULL,
# 							related_name = 'pos')
# 	po_type 		= models.CharField(max_length=20,choices=PO_TYPE_CHOICE,default=BTO)
# 	delivery_date	= models.DateTimeField(blank=True, null=True)
# 	delivery_address= models.TextField(null = True,blank = True)
# 	created_date	= models.DateTimeField(auto_now_add=True)
# 	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
# 	active			= models.BooleanField(default=True)
# 	started			= models.BooleanField(default=False)
# 	completed		= models.BooleanField(default=False)


# 	def __str__(self):
# 		return ('%s' % self.name)

# 	def order(self):
# 		return self.orderitems.order.name

# 	def weight(self):
# 		if self.product != None :
# 			return self.product.weight * self.qty
# 		return 0

# 	def weight_unit(self):
# 		if self.product != None :
# 			return self.product.weight_unit
# 		return ''

# 	def get_absolute_url(self):
# 		return reverse('po:detail', kwargs={'slug': self.slug})