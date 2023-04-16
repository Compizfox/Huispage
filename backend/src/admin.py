from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Debitor, Enrolment, Expense, ExpenseItem, Inhabitant, Meal, ExpenseCategory


class InhabitantInline(admin.StackedInline):
    model = Inhabitant
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (InhabitantInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register([Debitor, Enrolment, Expense, ExpenseItem, Meal, ExpenseCategory])
