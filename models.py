from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phonenumber = models.CharField(max_length=20, blank=True,default="00")
    gender = models.CharField(max_length=10, blank=True,default="m")
    birth_date = models.DateField(null=True, blank=True)
    # default_debit_account=models.IntegerField(null=True, blank=True)
    # default_credit_account=models.IntegerField(null=True, blank=True)
    admin=models.BooleanField(default=False)
    privillage=models.IntegerField(default=1)

    def __str__(self):
    	return str(self.id)+":"+str(self.username)

    class Meta:
    	ordering=('-id',)
    

		
class Business(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	business_name=models.CharField(max_length=40,)
	business_location=models.CharField(max_length=40,null=True,blank=True)
	business_phone=models.CharField(max_length=20,)
	business_nature=models.CharField(max_length=40,)
	business_email=models.EmailField(max_length=40,null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	def __str__(self):
		return str(self.id)+": "+str(self.business_name)

	

class Account(models.Model):
	business=models.ForeignKey(Business,on_delete=models.CASCADE)
	account_name=models.CharField(max_length=40,)
	account_balance=models.FloatField(max_length=40,null=True,blank=True,default=0.0)	
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	def __str__(self):
		return str(self.id)+": "+str(self.account_name)
	

	def save(self,*args,**kargs):
		print('Saving Account')
		if self.account_balance is None or '':
			print('warning balance is empty')	
		super(Account,self).save(*args,**kargs)


class DebitAccountManager(models.Manager):
	def all(self,*args,**kargs):
		query_set=super(DebitAccountManager,self).all(*args,**kargs)
		qs=query_set.filter(id__gte=16)

		return qs

# received cash
class DebitAccount(models.Model):
	account=models.ForeignKey(Account,on_delete=models.CASCADE)
	debit_from=models.CharField(max_length=40,)
	debit_amount=models.FloatField(max_length=40,default=0.0)	
	debit_reason=models.CharField(max_length=40,null=True,blank=True,)
	debit_type=models.CharField(max_length=40,null=True,blank=True,default="cash")	
	debit_credit=models.BooleanField(default=True,)
	# actual date of receiving payment
	debit_credit_date_actual=models.DateTimeField(null=True,blank=True)
	# date set to receive payment
	debit_credit_date_declared=models.DateTimeField(null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

	# objects=DebitAccountManager()

	def __str__(self):
		return str(self.id)+": "+str(self.debit_from)


	def save(self,*args,**kargs):
		print('Saving Account')
		if self.debit_credit is False:
			print('then payment date is created+a')	
		super(DebitAccount,self).save(*args,**kargs)

	# def all(self,*args,**kargs):
	# 	query_set=super(DebitAccount,self).all(*args,**kargs)
	# 	qs=query_set.filter(id=2)

	# 	return qs

	class Meta:
		ordering=['-id']


# spentcash
class CreditAccount(models.Model):
	account=models.ForeignKey(Account,on_delete=models.CASCADE)
	credit_to=models.CharField(max_length=40,)
	credit_amount=models.FloatField(max_length=40,default=0.0)	
	credit_reason=models.CharField(max_length=40,null=True,blank=True,)
	credit_type=models.CharField(max_length=40,null=True,blank=True,default="cash")	
	credit_credit=models.BooleanField(default=False,)
	# actual date of paying the extended loan
	credit_credit_date_actual=models.DateTimeField(null=True,blank=True)
	# date set to make  payment of loan
	credit_credit_date_declared=models.DateTimeField(null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	def __str__(self):
		return str(self.id)+": "+str(self.account_name)
	

	