from django.contrib import admin
from .models import Income
from .models import Expenses
from .models import Budget
from .models import Alerts
# Register your models here.
admin.site.register(Income)
admin.site.register(Budget)
admin.site.register(Expenses)
admin.site.register(Alerts)