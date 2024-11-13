from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Income(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  job = models.CharField(max_length= 100)
  amount= models.DecimalField(max_digits= 10, decimal_places= 2)
  date_received = models.DateField()
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  
class Budget(models.Model):
  user=models.ForeignKey(User, on_delete= models.CASCADE, null= True)
  category = models.CharField(max_length=100)
  amount_limit = models.DecimalField(max_digits= 10, decimal_places= 2)
  start_date = models.DateField()
  end_date = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Expenses(models.Model):
   user=models.ForeignKey(User, on_delete= models.CASCADE, null= True)
   category = models.CharField(max_length=100)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date_spent = models.DateField()
   description = models.TextField(blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

class Alerts(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
  budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='alerts')
  alert_amount = models.DecimalField(max_digits=10, decimal_places=2)  
  is_alert = models.BooleanField(default=False)
  alert_date = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)