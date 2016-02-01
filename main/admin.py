from django.contrib import admin

from main.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)