from rest_framework import serializers
from .models import Business,Account,DebitAccount,CreditAccount,User
# from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model =User
		fields ="__all__"

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model =Account
		fields ="__all__"

class CreditAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model =CreditAccount
		fields ="__all__"

class DebitAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model =DebitAccount
		fields ="__all__"

class BusinessSerializer(serializers.ModelSerializer):
	class Meta:
		model = Business
		fields= "__all__"






