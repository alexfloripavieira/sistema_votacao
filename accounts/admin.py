from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# Customização do User Admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'must_change_password', 'created_at')
    list_filter = ('must_change_password',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
