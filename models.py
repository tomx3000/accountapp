from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    phonenumber = models.CharField(max_length=20, blank=True,default="00")
    gender = models.CharField(max_length=10, blank=True,default="m")
    birth_date = models.DateField(null=True, blank=True)
    # default_debit_account=models.IntegerField(null=True, blank=True)
    # default_credit_account=models.IntegerField(null=True, blank=True)
    admin=models.BooleanField(default=False)
    privillage=models.IntegerField(default=1)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)
	
	
    def __str__(self):
    	return str(self.id)+":"+str(self.username)


    class Meta:
    	ordering=('-id',)
    
class Business(models.Model):
	owners=models.ManyToManyField(User,through='Ownership')
	business_name=models.CharField(max_length=40,)
	business_location=models.CharField(max_length=40,null=True,blank=True)
	business_phone=models.CharField(max_length=20,)
	business_nature=models.CharField(max_length=40,)
	business_email=models.EmailField(max_length=40,null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	def __str__(self):
		return str(self.id)+": "+str(self.business_name)

class Ownership(models.Model):
	business=models.ForeignKey(Business,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

	def __str__(self):
		return str(self.business.business_name)+": "+str(self.user.username)


class Account(models.Model):
	business=models.ForeignKey(Business,on_delete=models.CASCADE)
	account_name=models.CharField(max_length=40,)
	# amount saved to this bank account for this particular business as of the current updated time

	# this balance is only updated once daily after the bank confirms savings deposited 
	
	account_balance=models.FloatField(max_length=40,null=True,blank=True,default=0.0)
	bank_account_name=models.CharField(max_length=40,null=True,blank=True)
	bank_account_number=models.CharField(max_length=40,null=True,blank=True)	
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
# note the account here was initialy percived as the place where the business is going to sink money
# though, since then the account perception has changed to a plcae where the business references its savings
# thus better modification could be made on the db to put the business inplace of the account directly
# though no harm is done now, but for later when perfomance is an issue, this could be a point to start with

class DebitAccount(models.Model):
	account=models.ForeignKey(Account,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
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
# this is a cedit account transaction table
# note the account here was initialy percived as the place where the business is going to source money from
# though, since then the account perception has changed to a plcae where the business references its savings
# thus better modification could be made on the db to put the business inplace of the account directly
# though no harm is done now, but for later when perfomance is an issue, this could be a point to start with
class CreditAccount(models.Model):
	account=models.ForeignKey(Account,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	# make this field nullable
	# or remove it completely
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

	# adding duration for each payment 
	# options
		# daily, custom duration eg. mothnly etc (this applies for things like rent) , fixed ord one time cost things (eg assets like motot cycle), unknown duration (e.g electric bill, etc)

	# duration options={daily,custom,fixed,unknown}
	credit_duration_option=models.CharField(max_length=40,null=True,blank=True,default="daliy")
	
	# duration for which the amount paid is going to last eg. 6 month fro rent
	# duration should be stored in days
	credit_duration=models.FloatField(max_length=40,default=0.0)

	# calculate the equivalent daily cost for the amount paid
	# total amount spent is stored with credit_amount
	credit_daily_equivalent_cost=models.FloatField(max_length=40,default=0.0)	

	# current amount paid
	# this keeps track of payment made so far
	# for this particular item/transaction
	# it will only stop updating once it is equal with the credit_amount

	# NOte this should be removed once you figure out a method for calculating the amounts on the fly
	# ps: there should always be only one version of the truth
	credit_current_payment=models.FloatField(max_length=40,default=0.0)

	def __str__(self):
		return str(self.id)+": "+str(self.account.account_name)
	
	
# note this table was added on the fly, after the schema was designed

# so when you get time , revisit the schema and make sure it fits well

class StockCollection(models.Model):
	# note user here is to imply the person editing the stock collection and not the owner of the business
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	business=models.ForeignKey(Business,on_delete=models.CASCADE)
	amount=models.FloatField(default=0,null=True,blank=True)
	openingstock=models.BooleanField(default=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)
	
	class Meta:
		ordering=['-created_at']

