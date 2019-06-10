from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
# from django.db.models.signals import pre_save
# from django.db.models import Sum

# Create your models here.
from po.models import Po
class Delivery(models.Model):
	invoice 		= models.CharField(max_length=50,null = True,blank = True)
	po  			= models.ForeignKey(Po,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'deliverys')
	description 	= models.TextField(null = True,blank = True)
	qty				= models.IntegerField(default=0)
	delivery_date	= models.DateTimeField(blank=True, null=True)
	delivery_address= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % self.invoice)

	def get_absolute_url(self):
		return reverse('delivery:detail', kwargs={'pk': self.pk})


	# def job(self):
	# 	return self.jobs.count()

	# def total(self):
	# 	return self.jobs.aggregate(Sum('qty'))['qty__sum']

# def pre_save_po_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.name)

# pre_save.connect(pre_save_po_receiver, sender=Po)
