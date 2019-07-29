from django.contrib import admin

from .models import Employee, Employment

# Register your models here.

class EmploymentInline(admin.StackedInline):
    model = Employment
    can_delete = True
    extra = 0


class EmployeeAdmin(admin.ModelAdmin):
    inlines = (EmploymentInline, )
    search_fields = ('full_name', )


class EmploymentAdmin(admin.ModelAdmin):
    search_fields = (
        'number',
    )


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Employment, EmploymentAdmin)
