from django.shortcuts import get_object_or_404

from .models import Employee, Employment


class EmployeeContextMixin():
    """Добавляет объект Employee в контекст
    представлений Employment.
    """
    # Имя переменной для использования в контексте
    employee_context_object_name = 'employee'

    # Имя переданного аргумента в URLConf,
    # содержащего значение slug
    employee_slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Добавляет объект Employee в контекст
        представлений Employment.
        """
        if hasattr(self, 'employee'):
            context = {
                # Добавляем в контекст имеющися объект
                self.employee_context_object_name: self.employee,
            }
        else:
            # Извлекаем переданный slug
            employee_slug = self.kwargs.get(self.employee_slug_url_kwarg)
            # Получаем объект
            employee = get_object_or_404(
                Employee,
                slug__iexact=employee_slug,
            )
            # Добавляем в контекст
            context = {self.employee_context_object_name: employee, }
        context.update(kwargs)
        return super().get_context_data(**context)


class EmploymentGetObjectMixin():
    """Получает связаный с Employee объект Employment.
    """
    def get_object(self, queryset=None):
        """Возвращает связанный с Employee объект Employment.
        """
        # Получаем slug из аргументов переданных представлению
        employee_slug = self.kwargs.get(self.employee_slug_url_kwarg)
        employment_pk = self.kwargs.get(self.pk_url_kwarg)

        if employee_slug is None or employment_pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with "
                "either a employee slug  and a employment pk."
                % self.__class__.__name__
            )
        return get_object_or_404(
            Employment,
            pk=employment_pk,
            employee__slug__iexact=employee_slug,
        )
