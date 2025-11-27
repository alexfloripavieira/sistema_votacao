from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Customização do User Admin se necessário
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
