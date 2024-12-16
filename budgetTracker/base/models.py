from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db.models import Sum


# User Model

class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=email, name=name, phone=phone, is_active = True)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        user = self.create_user(email, name, phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

# Category Model
class Category(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    CATEGORY_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='categories')
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category_type})"
# Income Model
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 limit_choices_to={'category_type': 'Income'}, related_name='income')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"



# Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 limit_choices_to={'category_type': 'Expense'}, related_name='expenses')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    is_fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"


# EMI Model
class EMI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emis')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=20) 
    description = models.TextField(blank=True, null=True)
    next_payment_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - EMI {self.amount} - {self.frequency}"


# Budget Model
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to= { 'category_type' : 'expense'})
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.email} - {self.category.name} Budget {self.amount_limit}"
    def is_exceeded(self):
        total_expenses = Expense.objects.filter(
            user=self.user,
            category=self.category,
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return total_expenses > self.amount_limit

# Alert Model
class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Alert for {self.user.email}: {self.message[:30]}"


# Report Model
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.user.email} - {self.report_type}" 
    
