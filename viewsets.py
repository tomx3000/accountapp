from rest_framework import viewsets,filters
from .models import Business,Account,DebitAccount,CreditAccount,User,Ownership,StockCollection
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from django.core.mail import send_mail
from .serializers import UserSerializer,AccountSerializer,CreditAccountSerializer,DebitAccountSerializer,BusinessSerializer,OwnershipSerializer,StockCollectionSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .csrfexempt import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from django.contrib.auth.models import User 
from django.contrib import messages

class AccountViewSet(viewsets.ModelViewSet):
	queryset=Account.objects.all()
	serializer_class=AccountSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def list(self,request):
		userid=request.user.id
		user=User.objects.get(id=userid)
		qs=Account.objects.filter(business__owners=user)
		serializer=AccountSerializer(qs,many=True)

		return Response(serializer.data)

class BusinessViewSet(viewsets.ModelViewSet):
	queryset=Business.objects.all()
	serializer_class=BusinessSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def list(self,request):
		userid=request.user.id
		user=User.objects.get(id=userid)
		qs=Business.objects.filter(owners=user)
		serializer=BusinessSerializer(qs,many=True)

		return Response(serializer.data)


class OwnershipViewSet(viewsets.ModelViewSet):
	queryset=User.objects.all()
	serializer_class=OwnershipSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class UserViewSet(viewsets.ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def create(self,request):
		print('gotcha create something')
		import random
		import string

		def generateRoandom(size=4,chars=string.ascii_lowercase+string.ascii_uppercase+string.digits):

			return ''.join(random.choice(chars) for _ in range(size))

		user=None

		while(not user):
			username = request.data.get('first_name')+''+generateRoandom(3)

			password=generateRoandom(8)
			email=request.data.get('first_name')+'@gmail.com'
			user = User.objects.create_user(username, email, password)
			User.objects.filter(id=user.id).update(privillage=request.data.get('privillage'),phonenumber=request.data.get('phonenumber'),created_by=request.user,first_name=request.data.get('first_name'))

		send_mail(
			    'New Partner',
			    'Raisisha \n firstname :'+request.data.get('first_name')+'\n'+'username :'+username+'\n password: '+password,
			    'info.company.tz@gmail.com',
			    [request.user.email],
			    fail_silently=False,
			   	
			)

		return Response({'username':username,'password':'password'})

	def destroy(self,request,pk=None):
		User.objects.filter(id=pk).delete()

		# return super().destroy(request)
		return Response('ok')

	def list(self,request):
		userid=request.user.id
		qs=User.objects.filter(id=userid)
		serializer=UserSerializer(qs,many=True)

		return Response(serializer.data)

class DebitAccountViewSet(viewsets.ModelViewSet):
	queryset=DebitAccount.objects.all()
	serializer_class=DebitAccountSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def list(self,request):
		userid=request.user.id
		user=User.objects.get(id=userid)
		qs=DebitAccount.objects.filter(account__business__owners=user)
		serializer=DebitAccountSerializer(qs,many=True)

		return Response(serializer.data)

	
class CreditAccountViewSet(viewsets.ModelViewSet):
	queryset=CreditAccount.objects.all()
	serializer_class=CreditAccountSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)


	def list(self,request):
		userid=request.user.id
		user=User.objects.get(id=userid)
		qs=CreditAccount.objects.filter(account__business__owners=user)
		serializer=CreditAccountSerializer(qs,many=True)

		return Response(serializer.data)


class StockViewSet(viewsets.ModelViewSet):
	queryset=StockCollection.objects.all()
	serializer_class=StockCollectionSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def list(self,request):
		userid=request.user.id
		user=User.objects.get(id=userid)
		qs=StockCollection.objects.filter(business__owners=user)
		serializer=StockCollectionSerializer(qs,many=True)

		return Response(serializer.data)

    
	