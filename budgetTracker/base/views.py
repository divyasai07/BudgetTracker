from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm, CustomUserChangeForm
from . import models
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Income, Expense, EMI, Budget, Alert, Report
from .forms import CustomAuthenticationForm,EMIForm
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
        description = request.POST['description']
        date = request.POST['date']
        category_id = request.POST['category']
        
        category = Category.objects.get(id=category_id)
        
        Expense.objects.create(amount=amount, description=description, date=date, category=category, user=request.user)

        return redirect("home")
    
    
    categories = Category.objects.filter(category_type="expense", user=request.user)
    print("Categories passed to template:", categories) 
    context = {'categories': categories}
    return render(request, 'addExpense.html', context)



def income(request):
    
    incomes = Income.objects.filter(user=request.user)
    expenses= Expense.objects.filter(user=request.user)
    context = {'incomes': incomes, 'expenses':expenses}
    return render(request, 'income.html', context)

    
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_type = request.POST.get('category_type')  
        return_url = request.POST.get('return_url', 'income') 
        
        if name and category_type:
          
            if not Category.objects.filter(name=name, category_type=category_type, user=request.user).exists():
                Category.objects.create(
                    name=name,
                    category_type=category_type,
                    user=request.user
                )
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
def delete_expense(request):
    if expense.category.name == "EMI":
        return HttpResponseForbidden("EMI cannot be deleted.")
    if request.method == 'POST':
        expense_id= request.POST.get('expense_id')
        try:
            expense= Expense.objects.get(id=expense_id)
            expense.delete()
        except Expense.DoesNotExist:
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

def update_expense(request,expense_id):
    expense=get_object_or_404(Expense,id=expense_id,user=request.user)
    categories= Category.objects.filter(category_type= "expense",user=request.user)
    if expense.category.name == "EMI":
        return HttpResponseForbidden("EMI cannot be updated.")
    if request.method == "POST":
        expense.amount= request.POST['amount']
        expense.description= request.POST['description']
        expense.date= request.POST['date']
        expense.category_id = request.POST['category']
        
        expense.save()
        return redirect('income')
    context = {'expense': expense, 'categories':categories}
    return render(request,'updateExpense.html',context)

def emi_list(request):
    emis = EMI.objects.filter(user=request.user)
    return render(request, 'emi_list.html', {'emis': emis})
 


def add_emi(request):
    if request.method == 'POST':
        form = EMIForm(request.POST)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user 
            emi.save()
            emi_category, created = Category.objects.get_or_create(
                name="EMI",  
                defaults={'user': request.user}  
            )
            Expense.objects.create(
                user=request.user,
                amount=emi.amount,
                description=f"EMI for {emi.description or 'N/A'}",
                date=emi.next_payment_date,
                category=emi_category 
            )

            return redirect('emi_list')  
    else:
        form = EMIForm()
    return render(request, 'add_emi.html', {'form': form})

