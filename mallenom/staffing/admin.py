from django.contrib import admin

from .models import Department, Position, Staffing

# Register your models here.

class StaffingInline(admin.StackedInline):
    model = Staffing
    can_delete = True
    extra = 0


class DepartmentAdmin(admin.ModelAdmin):
    inlines = (StaffingInline, )
    search_fields = ('name', )


class PositionAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class StaffingAdmin(admin.ModelAdmin):
    search_fields = (
        'department__name',
        'position__name',
        'count',
    )


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Staffing, StaffingAdmin)
