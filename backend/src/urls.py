"""Huispage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import (
	InhabitantList,
	InhabitantViewSet,
	ExpenseViewSet,
	ExpenseCategoryViewSet,
	EnrolmentViewSet,
	DailiesView,
	MealViewSet,
	ExpenseImportView,
	get_balance,
	set_csrf_token, login, logout)

router = routers.SimpleRouter()
router.register('admin/inhabitants',  InhabitantViewSet)
router.register('expenses', ExpenseViewSet)
router.register('expense_categories', ExpenseCategoryViewSet)
router.register('enrolments', EnrolmentViewSet)
router.register('meals', MealViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),

	path('api/dailies/<int:year>/<int:week>/', DailiesView.as_view()),
	path('api/admin/expensesimport/', ExpenseImportView.as_view()),
	path('api/balance/', get_balance),

	path('api/inhabitants/', InhabitantList.as_view()),

	path('api/auth/set_csrf_token', set_csrf_token),
	path('api/auth/login', login),
	path('api/auth/logout', logout),

	path('api/', include(router.urls)),
]
