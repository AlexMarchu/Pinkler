from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PinklerUser


class PinklerUserAdmin(UserAdmin):
    model = PinklerUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'sex', 'status', 'birthday', 'avatar',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'sex', 'status', 'birthday', 'avatar',)}),
    )


admin.site.register(PinklerUser, PinklerUserAdmin)
