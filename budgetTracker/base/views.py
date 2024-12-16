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
from .forms import CustomAuthenticationForm,EMIForm, BudgetForm
from django.contrib.auth import authenticate
from base.models import User
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.db.models import Sum
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
    total_incomes= Income.objects.filter(user= request.user).aggregate(total = models.Sum('amount'))['total'] or 0
    total_expenses= Expense.objects.filter(user=request.user).aggregate(total= models.Sum('amount'))['total'] or 0
    context = {
        'name': request.user.name,
        'res': res ,
        'total_incomes': total_incomes ,
        'total_expenses': total_expenses
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
        budget= Budget.objects.filter(category=category).first()
        
        Expense.objects.create(amount=amount, description=description, date=date, category=category, user=request.user)
        total_expenses = Expense.objects.filter(user=request.user, category=category).aggregate(total=models.Sum('amount'))['total'] or 0
        if budget:
         if total_expenses > budget.amount_limit:
           message = (
        f"Your Budget exceeded for {budget.category.name}. "
        f"Your Budget limit is {budget.amount_limit} while your expenses are {total_expenses}."
           )
           if not Alert.objects.filter(user=request.user, message=message, is_read=False).exists():
                Alert.objects.create(
                    user=request.user,
                    message=message
                )
           unread_alerts = Alert.objects.filter(user=request.user, is_read=False)
           alert_count = unread_alerts.count()
           name= request.user.name
           context={
               
               'alerts':unread_alerts,
               'alert_count':alert_count,
               'name':name,
               

            }
    
           return render(request, "budget_status.html", 
        context)
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
    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)

        if expense.category.name == "EMI":
            return HttpResponseForbidden("EMI cannot be deleted.")

        expense.delete()
        

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

def set_budget(request):
    
    categories = Category.objects.filter(user=request.user, category_type='expense').values('id', 'name')

    if request.method == 'POST':
        category_id = request.POST.get('category')
        amount = request.POST.get('amount_limit')
        if category_id and amount:
            try:
                
                category = Category.objects.get(id=category_id)
                amount = float(amount)

                Budget.objects.create(user=request.user, category=category, amount_limit=amount)
                messages.success(request, "Budget has been set successfully")
                return redirect(set_budget)
            except Category.DoesNotExist:
                messages.error(request, "Selected category does not exist")
            
    return render(request, "budget.html", {'categories': categories})


from .models import Budget

def check_budget(request):
    budgets = Budget.objects.filter(user=request.user)
    notifications = []  
    
    for budget in budgets:
        total_expenses = Expense.objects.filter(user=request.user, category=budget.category).aggregate(total=models.Sum('amount'))['total'] or 0
        if total_expenses> budget.amount_limit:
             message = (
        f"Your Budget exceeded for {budget.category.name}. "
        f"Your Budget limit is {budget.amount_limit} while your expenses are {total_expenses}."
           )
            
             if not Alert.objects.filter(user=request.user, message=message, is_read=False).exists():
                Alert.objects.create(
                    user=request.user,
                    message=message
                )
    
    
    unread_alerts = Alert.objects.filter(user=request.user, is_read=False)
    alert_count = unread_alerts.count()
    name= request.user.name
    context={
      'budgets':budgets,
      'alerts':unread_alerts,
       'alert_count':alert_count,
       'name':name,
       

    }
    
    return render(request, "budget_status.html", 
        context)

def notifications_view(request):
    notifications = Alert.objects.filter(user=request.user)
   
    Alert.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'budget_status.html', {'notifications': notifications})


def send_notification(budget):
    send_mail('budget limit exceeded',f"your budget for {budget.category.name} has crossed",[budget.user.email],fail_silently= False)

def report(request):
    labels=[]
    data=[]
    labels2=[]
    data2=[]
    incomes = Income.objects.filter(user=request.user).values('category__name').annotate(income_Sum= Sum('amount'))
    expenses= Expense.objects.filter(user= request.user).values('category__name').annotate(expense_sum=Sum('amount'))
    for income in incomes:
        labels.append(income['category__name'])
        data.append(float(income['income_Sum']))
    for expense in expenses:
        labels2.append(expense['category__name'])
        data2.append(float(expense['expense_sum']))
    
    context={
        'labels' : json.dumps(labels),
        'data' : json.dumps(data),
        'labels2': json.dumps(labels2),
        'data2': json.dumps(data2)
    }
    print("Labels:", labels)
    print("Data:", data)
    print("Labels2:", labels2)
    print("Data2:", data2)
    return render(request, 'report.html', context)