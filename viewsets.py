from rest_framework import viewsets,filters
from .models import Business,Account,DebitAccount,CreditAccount,User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from django.core.mail import send_mail
from .serializers import UserSerializer,AccountSerializer,CreditAccountSerializer,DebitAccountSerializer,BusinessSerializer

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
		qs=Account.objects.filter(business__user=user)
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
		qs=Business.objects.filter(user=user)
		serializer=BusinessSerializer(qs,many=True)

		return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

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
		qs=DebitAccount.objects.filter(account__business__user=user)
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
		qs=CreditAccount.objects.filter(account__business__user=user)
		serializer=CreditAccountSerializer(qs,many=True)

		return Response(serializer.data)




    
	