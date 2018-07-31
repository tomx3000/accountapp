from django.conf.urls import url
from django.urls import  path,include

from .views import Home,LoginUser,ExpensePage,ProfilePage,BusinessPage,SettingsPage,AcceptDebit,RegisterUser,ChangeUsername,ChangePassword,SalesPage,Clients,getUser,getBusiness,getCredit,getDebit,getAccount


urlpatterns = [
# sales
path('', Home,name='home'),
path('sales/', SalesPage,name='sales'),


# login page
path('login/', LoginUser,name='login'),
# expenses
path('expense/', ExpensePage,name='expense'),
# personal ptofile
path('profile/', ProfilePage,name='profile'),
# business profile
path('business/', BusinessPage,name='business'),
# system settings 
path('setting/', SettingsPage,name='settings'),
path('registeruser/<slug:username>/<slug:phonenumber>/<slug:firstpassword>/<slug:secondpassword>/', RegisterUser,name='userregister'),


path('debitaccount/<slug:id>/', AcceptDebit,name='acceptdebit'),

path('username/<slug:id>/<slug:username>/', ChangeUsername),
path('userpass/<slug:id>/<slug:oldpassword>/<slug:firstnewpassword>/<slug:secondnewpassword>/<slug:username>/', ChangePassword),

path('clients/', Clients,name='clients'),


# get models for that user
path('get/user/', getUser,name='getuser'),
path('get/business/<slug:id>/', getBusiness,name='getbusiness'),
path('get/credit/<slug:id>/', getCredit,name='getcredit'),
path('get/debit/<slug:id>/', getDebit,name='getdebit'),
path('get/account/<slug:id>/', getAccount,name='getaccount'),


]