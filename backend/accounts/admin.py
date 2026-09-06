from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# VARSHA admin branding
admin.site.site_header = 'VARSHA KRITRIMA BUDDHIH — Administration'
admin.site.site_title = 'VARSHA Admin'
admin.site.index_title = 'VARSHA KRITRIMA BUDDHIH Control Panel'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'mobile', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (('VARSHA Profile', {'fields': ('mobile', 'role')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('VARSHA Profile', {'fields': ('email', 'mobile', 'role')}),)
