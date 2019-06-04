from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Sum
# from django.db.models import Sum

# Create your models here.
from po.models 		import Po
from product.models import Product

class Order(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	# qty				= models.IntegerField(default=0)
	product			= models.ForeignKey(Product,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'orders')
	# pos 			= models.ManyToManyField(
	# 						Po,
	# 						through='PoMembership',
	# 						through_fields=('order', 'po'))
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	draft			= models.BooleanField(default=True)
	active			= models.BooleanField(default=True)
	completed		= models.BooleanField(default=False)


	def __str__(self):
		return ('%s' % self.name)

	def pos(self):
		return self.orderitems.count()

	def weight(self):
		if self.product != None :
			return self.product.weight * self.qty()
		return 0

	def qty(self):
		if self.orderitems.count()>0 :
			return self.orderitems.aggregate(Sum('po__qty'))['po__qty__sum']
		return 0

	def get_absolute_url(self):
		# return 'test'
		return reverse('order:detail', kwargs={'slug': self.slug})

	# def total(self):
	# 	return self.jobs.aggregate(Sum('qty'))['qty__sum']

def pre_save_order_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.name)

pre_save.connect(pre_save_order_receiver, sender=Order)


class OrderItem(models.Model):
	order 			= models.ForeignKey(Order, 
								on_delete=models.CASCADE,
								related_name='orderitems')
	po 				= models.OneToOneField(Po, 
								on_delete=models.CASCADE,
								related_name='orderitems')
	seq				= models.IntegerField(default=1)
	note			= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	completed		= models.BooleanField(default=False)

	def __str__(self):
		return ('%s-%s' % (self.seq,self.po))

	def qty(self):
		return self.po.qty



# from django.db import models

# class Person(models.Model):
#     name = models.CharField(max_length=50)

# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(
#         Person,
#         through='Membership',
#         through_fields=('group', 'person'),
#     )

# class Membership(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     inviter = models.ForeignKey(
#         Person,
#         on_delete=models.CASCADE,
#         related_name="membership_invites",
#     )
#     invite_reason = models.CharField(max_length=64)