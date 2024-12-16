"""
URL configuration for budgetTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.register, name="register"),
    path("login",views.login,name="login"),
    path("home",views.home,name="home"),
    path("logout",views.logout,name="logout"),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('income/', views.income, name='income'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_income/',views.delete_income,name='delete_income'),
    path('update_income/<int:income_id>/', views.update_income, name='update_income'),
    path('delete_expense/',views.delete_expense,name='delete_expense'),
    path('update_expense/<int:expense_id>/', views.update_expense, name='update_expense'),
    path('add-emi/', views.add_emi, name='add_emi'),
    path('emis/', views.emi_list, name='emi_list'),
    path('set_budget/',views.set_budget, name='set_budget'),
    path('check_budget/', views.check_budget, name='check_budget'),
    path('report/', views.report,name="report")
]
