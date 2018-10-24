from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Business,Account,DebitAccount,CreditAccount,User,Ownership,StockCollection
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from django.http import JsonResponse


from .serializers import UserSerializer,AccountSerializer,CreditAccountSerializer,DebitAccountSerializer,BusinessSerializer,OwnershipSerializer
from django.db.models import Q

from django.utils.translation import gettext as _
# Create your views here.
from django.utils import timezone
from datetime import timedelta
import datetime


@csrf_exempt
@login_required(login_url='/login/')
def stockAdd(request,*args,**kargs):

	if kargs['opening'] == 'true':
		kargs['opening']=True
	else: 
		kargs['opening']=False

	today=datetime.date.today()

	tomorrow=today+timedelta(days=1)
	user=User.objects.get(id=kargs['user'])
	business=Business.objects.get(id=kargs['bussiness'])

	stock_today=StockCollection.objects.filter(created_at__gte=today,created_at__lt=tomorrow,business=business,openingstock=kargs['opening'])

	if(stock_today.count()<1):
		print("Creating new stock")
		
		new_stock_entry=StockCollection.objects.create(amount=kargs['amount'],openingstock=kargs['opening'],user=user,business=business)
		new_stock_entry.save()

	else:
		print("Updating existing stock")
		# to improve performance , you can remove the update of the business, since its never gona happen for the user to change the business
		
		stock_today.update(amount=kargs['amount'],openingstock=kargs['opening'],user=user,business=business)

	# the algorithm pseudo
	# check if the opening/closing stock for the day is present
	# if yes update the current stock with the new amount
	# if no create a new stock

	return HttpResponse('ok')

@login_required(login_url='/login/')
def Clients(request,*args,**kargs):
	# user = request.user
	if request.user.admin:
		return render(request,'clients.html')
	else:
		return redirect('home')
	

@login_required(login_url='/login/')
def Home(request,*args,**kargs):
	# user = request.user

	# this set the language in the session
	# from django.utils import translation
	# user_language = 'sw'
	# translation.activate(user_language)
	# request.session[translation.LANGUAGE_SESSION_KEY] = user_language

	# remove the language from the session and allows for the site to use the langusge sent b the browser header 
	# if translation.LANGUAGE_SESSION_KEY in request.session:
	# 	del request.session[translation.LANGUAGE_SESSION_KEY]
	
	return render(request,'home.html')

@login_required(login_url='/login/')
def SalesPage(request,*args,**kargs):
	# user = request.user
	
	return render(request,'sales.html')


def LoginUser(request,*args,**kargs):
	if(request.method=='POST'):

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:

		    login(request, user)

		    # logout(request)
		    return redirect('home')

		else:
			return render(request,'login.html',{})	

	elif(request.method=='GET'):
		logout(request)
		return render(request,'login.html')	


@csrf_exempt
@login_required(login_url='/login/')
def checkOwnership(request,*args,**kargs):
	print('reached check ownership')
	user=User.objects.get(id=kargs['userid'])
	business=Business.objects.get(id=kargs['businesid'])
	qs=Ownership.objects.filter(user=user,business=business)
	if(qs.count()>=1):
		print('ok')
		return HttpResponse('ok')
	else:
		print('not okay')
		return HttpResponse('not okay')

@csrf_exempt
@login_required(login_url='/login/')
def RemoveOwnership(request,*args,**kargs):
	user=User.objects.get(id=kargs['userid'])
	business=Business.objects.get(id=kargs['businesid'])
	Ownership.objects.filter(user=user,business=business).delete()
	
	return HttpResponse('ok')
		


@csrf_exempt
@login_required(login_url='/login/')
def getUser(request,*args,**kargs):
	qs=User.objects.all()
	serializer=UserSerializer(qs,many=True)
	return JsonResponse(serializer.data,safe=False)

@csrf_exempt
@login_required(login_url='/login/')
def getMyUsers(request,*args,**kargs):
	# qs=User.objects.filter(Q(created_by=request.user) | Q(id=request.user))	
	qs=User.objects.filter(created_by=request.user)
	serializer=UserSerializer(qs,many=True)
	return JsonResponse(serializer.data,safe=False)


@csrf_exempt
@login_required(login_url='/login/')
def getMyUsersBuz(request,*args,**kargs):
	qs=Ownership.objects.filter(Q(user__created_by=request.user)|Q(user=request.user))
	serializer=OwnershipSerializer(qs,many=True)
	return JsonResponse(serializer.data,safe=False)


@csrf_exempt
@login_required(login_url='/login/')
def getBusiness(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=Business.objects.filter(owners=user)
	serializer=BusinessSerializer(qs,many=True)

	return JsonResponse(serializer.data,safe=False)
	


@csrf_exempt
@login_required(login_url='/login/')
def getCredit(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=CreditAccount.objects.filter(account__business__owners=user)
	serializer=CreditAccountSerializer(qs,many=True)

	return JsonResponse(serializer.data,safe=False)

@csrf_exempt
@login_required(login_url='/login/')
def getDebit(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=DebitAccount.objects.filter(account__business__owners=user)
	serializer=DebitAccountSerializer(qs,many=True)
	return JsonResponse(serializer.data,safe=False)


@csrf_exempt
@login_required(login_url='/login/')
def getAccount(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=Account.objects.filter(business__owners=user)
	serializer=AccountSerializer(qs,many=True)

	return JsonResponse(serializer.data,safe=False)



@csrf_exempt
@login_required(login_url='/login/')
def ChangePassword(request,*args,**kargs):
	user = authenticate(request, username=kargs['username'], password=kargs['oldpassword'])

	if user is not None:

		if kargs['firstnewpassword'] == kargs['secondnewpassword']:		
			user.set_password(kargs['firstnewpassword'])
			user.save()
			return HttpResponse('good')
		else:
			return HttpResponse('notmatched')

	else:
		return HttpResponse('badold')

@csrf_exempt
@login_required(login_url='/login/')
def ChangeUsername(request,*args,**kargs):
	try:
		user=User.objects.get(username=kargs['username'])

	except Exception as e:
		User.objects.filter(id=kargs['id']).update(username=kargs['username'])
		return HttpResponse('good')
	else:
		return HttpResponse('bad')



@login_required(login_url='/login/')
def ExpensePage(request,*args,**kargs):
	# user = request.user
	
	return render(request,'expense.html')


@login_required(login_url='/login/')
def ProfilePage(request,*args,**kargs):
	# user = request.user
	
	return render(request,'profile.html')


@login_required(login_url='/login/')
def BusinessPage(request,*args,**kargs):
	# user = request.user
	
	return render(request,'bussiness.html')


@login_required(login_url='/login/')
def SettingsPage(request,*args,**kargs):
	# user = request.user
	
	return render(request,'setting.html')

@csrf_exempt
@login_required(login_url='/login/')
def AcceptDebit(request,*args,**kargs):

	sale=DebitAccount.objects.filter(id=kargs['id'])
	updatesale=sale.update(debit_credit=False,user=request.user)
	# print(request.POST)
	return HttpResponse('ok')



@csrf_exempt
# @login_required(login_url='login/')
def RegisterUser(request,*args,**kargs):

	print('gotcha create something')
	import random
	import string

	
	user=None
	if kargs['firstpassword'] == kargs['secondpassword']:	
		password=kargs['firstpassword']
	else:
		return HttpResponse('badpasswords')

	username = kargs['username']

	email=username+'@gmail.com'
	try:

		user = User.objects.create_user(username, email, password)
	except Exception as e:
		return HttpResponse('badusername')

	else:
		return HttpResponse('ok')
			
# print(request.POST)

def option_daily_select(*args,**kargs):
	user=User.objects.get(id=kargs['userid'])
	qs=CreditAccount.objects.filter(account__business__owners=user,id=kargs["creditid"]).update(credit_amount=kargs["amount"],credit_duration_option="daily")
	# update the credit_duration_option with daily
	# just update the credit_amount

	pass

# use this to convert the durations into seconds
def get_duration(*args,**kargs):
	duration =0
	# use time daelta to calculate the respective duration in seconds
	return	duration

def get_daily_cost(*args,**kargs):
	daily_eq=0
	return daily_eq

def option_custom_select(*args,**kargs):
	user=User.objects.get(id=kargs['userid'])
	qs=CreditAccount.objects.filter(account__business__owners=user,id=kargs["creditid"]).update(credit_amount=kargs["amount"],credit_duration_option="custom",credit_duration=get_duration(args,kargs),credit_daily_equivalent_cost=get_daily_cost(args,kargs))

	# update the credit_duration_option with custom
	# uodate the credit)duration with the equvalent time in seconds
	# update the credit_daily_equivalent_cost with the calculted daily value of the amount in credit_amount
	# 
	pass

def option_fixed_select(*args,**kargs):
	user=User.objects.get(id=kargs['userid'])
	qs=CreditAccount.objects.filter(account__business__owners=user,id=kargs["creditid"]).update(credit_amount=kargs["amount"],credit_duration_option="fixed",credit_duration=get_duration(args,kargs),credit_daily_equivalent_cost=get_daily_cost(args,kargs))

	pass

def option_unknown_select(*args,**kargs):
	user=User.objects.get(id=kargs['userid'])
	qs=CreditAccount.objects.filter(account__business__owners=user,id=kargs["creditid"]).update(credit_amount=kargs["amount"],credit_duration_option="unknown")
	pass


def option_daily_update():

	pass

def option_custom_update():
	pass


def option_fixed_update():
	pass

def option_unknown_update():
	pass




