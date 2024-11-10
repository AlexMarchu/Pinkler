from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PinklerUser, UserThemePreference

class PinklerUserAdmin(UserAdmin):
    model = PinklerUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'sex', 'status', 'birthday', 'avatar',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'sex', 'status', 'birthday', 'avatar',)}),
    )

class UserThemePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'font_size', 'primary_color')

admin.site.register(UserThemePreference, UserThemePreferenceAdmin)
admin.site.register(PinklerUser, PinklerUserAdmin)