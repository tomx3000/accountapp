from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Business,Account,DebitAccount,CreditAccount,User


admin.site.register(Business)
admin.site.register(Account)
admin.site.register(DebitAccount)
admin.site.register(CreditAccount)
admin.site.register(User)



