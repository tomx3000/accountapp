from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Business,Account,DebitAccount,CreditAccount,User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from django.http import JsonResponse


from .serializers import UserSerializer,AccountSerializer,CreditAccountSerializer,DebitAccountSerializer,BusinessSerializer
# Create your views here.

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
def getUser(request,*args,**kargs):
	qs=User.objects.all()
	serializer=UserSerializer(qs,many=True)
	return JsonResponse(serializer.data,safe=False)

@csrf_exempt
@login_required(login_url='/login/')
def getBusiness(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=Business.objects.filter(user=user)
	serializer=BusinessSerializer(qs,many=True)

	return JsonResponse(serializer.data,safe=False)
	

@csrf_exempt
@login_required(login_url='/login/')
def getCredit(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=CreditAccount.objects.filter(account__business__user=user)
	serializer=CreditAccountSerializer(qs,many=True)

	return JsonResponse(serializer.data,safe=False)

@csrf_exempt
@login_required(login_url='/login/')
def getDebit(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=DebitAccount.objects.filter(account__business__user=user)
	serializer=DebitAccountSerializer(qs,many=True)
	return JsonResponse(serializer.data,safe=False)


@csrf_exempt
@login_required(login_url='/login/')
def getAccount(request,*args,**kargs):
	user=User.objects.get(id=kargs['id'])
	qs=Account.objects.filter(business__user=user)
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
	updatesale=sale.update(debit_credit=False)
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
		return HttpResponse('notmatched')

	username = kargs['username']

	email=username+'@gmail.com'
	user = User.objects.create_user(username, email, password)

	if(user):
		return HttpResponse('ok')

	else:
		return HttpResponse('try onother username')
	
# print(request.POST)
	