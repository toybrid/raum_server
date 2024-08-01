from django.contrib import admin
from . models import User, AuthUserToken

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','username',]

class AuthUserTokenAdmin(admin.ModelAdmin):
    list_display = ['id','user','created_at','expires_at']


admin.site.register(User, UserAdmin)
admin.site.register(AuthUserToken, AuthUserTokenAdmin)