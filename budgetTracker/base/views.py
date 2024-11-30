from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm, CustomUserChangeForm
from . import models
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Income, Expense, EMI, Budget, Alert, Report
from .forms import CustomAuthenticationForm
from django.contrib.auth import authenticate
from base.models import User
from django.http import JsonResponse
import json


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
        
            
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']

        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            print(f"Authenticated User: {user}")  
            auth_login(request, user)
            return redirect('home') 
        else:
            messages.info(request,'invalid credentials')
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
@login_required
def home(request):
    print(f"User: {request.user}")  
    res = models.User.objects.filter(name=request.user)
    context = {
        'name': request.user.name,
        'res': res  
    }
    return render(request, 'home.html', context)

def logout(request):
   auth.logout(request)
   return redirect('register')

def add_income(request):
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)

        Income.objects.create(
            amount=amount,
            description=description,
            date=date,
            category=category,
            user=request.user
        )
        return redirect('income')

    categories = Category.objects.filter(category_type=Category.INCOME, user=request.user)

    context = {'categories': categories}
    return render(request, 'addIncome.html', context)

    
def add_expense(request):
    if request.method == "POST":
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        date = request.POST['date']
        Expense.objects.create(amount=amount, category= category, description= description, date=date)
        return redirect('home')  


def income(request):
    
    incomes = Income.objects.filter(user=request.user)

    context = {'incomes': incomes}
    return render(request, 'income.html', context)



#def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        category_type = request.POST['category_type']

        Category.objects.create(
            name=name,
            category_type=category_type,
            user=request.user
        )
        return redirect('add_income')
    
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        category_type = request.POST['category_type']
        if name and category_type:
            Category.objects.create(
                name=name,
                category_type=category_type,
                user=request.user
            )
        # Redirect back to the page where the user came from
        return_url = request.POST.get('return_url', 'income')
        return redirect(return_url)
    return redirect('income')

def delete_income(request):
    if request.method == 'POST':
        income_id = request.POST.get('income_id')
        try:
            income = Income.objects.get(id=income_id)
            income.delete() 
        except Income.DoesNotExist:
            pass 
    return redirect('income')


def update_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    categories = Category.objects.filter(category_type=Category.INCOME, user=request.user)
    if request.method == "POST":
        income.amount = request.POST['amount']
        income.description = request.POST['description']
        income.date = request.POST['date']
        income.category_id = request.POST['category']
        income.save()
        return redirect('income')
    context = {'income': income, 'categories': categories}
    return render(request, 'updateIncome.html', context)