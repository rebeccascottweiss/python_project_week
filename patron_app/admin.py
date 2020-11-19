from django.contrib import admin
from .models import Payment, Patron, Identification
#from ../bar_app/models import EmployeeManager, Bar, Drink, Employee, Tab, LineItem

# Register your models here.

admin.site.site_header = "Trey's playground"

admin.site.register(Patron)
admin.site.register(Payment)
admin.site.register(Identification)
#admin.site.register(EmployeeManager)
# admin.site.register(Bar)
# admin.site.register(Drink)
# admin.site.register(Employee)
# admin.site.register(Tab)
# admin.site.register(LineItem)