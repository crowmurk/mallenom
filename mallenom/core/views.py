from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import ProtectedError
from django.utils.translation import ugettext_lazy as _

# Create your views here.

class ActionTableDeleteMixin:
    action_table_model = None
    action_table_button = "action-table-button"
    action_table_success_message = None
    action_table_error_message = None
    action_table_multitables = None

    def post(self, request, *args, **kwargs):
        if self.action_table_model:
            self.action_table_multitables = [
                {
                    'model': self.action_table_model,
                    'button': self.action_table_button,
                    'success_message': self.action_table_success_message,
                    'error_message': self.action_table_error_message,
                }
            ]
        elif self.action_table_multitables:
            for action_table in self.action_table_multitables:
                if not action_table.get('model'):
                    raise ImproperlyConfigured(
                        "You must specify model in action_table_multitables"
                        " ({class_name}) to configure {mixin_name}".format(
                            class_name=self.__class__,
                            mixin_name=__class__.__name__,
                        )
                    )
        else:
            raise ImproperlyConfigured(
                "You must specify action_table_model or action_table_multitables"
                " ({class_name}) to configure {mixin_name}".format(
                    class_name=self.__class__,
                    mixin_name=__class__.__name__,
                )
            )

        for action_table in self.action_table_multitables:
            model = action_table['model']
            button = action_table['button']
            error_message = action_table['error_message']
            success_message = action_table['success_message']

            if not success_message:
                success_message = _("{name} were deleted successfuly").format(
                    name=model._meta.verbose_name_plural
                )

            if not error_message:
                error_message = _("Cannot delete {name} because of"
                                  " foreign references").format(
                                      name=model._meta.verbose_name_plural
                                  )

            button = request.POST.get(button)
            pks = request.POST.getlist(button)
            if pks:
                selected_objects = model.objects.filter(pk__in=pks)
                try:
                    selected_objects.delete()
                    messages.success(request, success_message)
                except ProtectedError:
                    messages.error(request, error_message)

        return HttpResponseRedirect(request.path)


class DeleteMessageMixin:
    success_message = None
    error_message = None

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
            if self.success_message:
                success_message = self.success_message
            else:
                success_message = _("{name} was deleted successfuly").format(
                    name=self.model._meta.verbose_name
                )
            messages.success(self.request, success_message)
        except ProtectedError:
            if self.error_message:
                error_message = self.error_message
            else:
                error_message = _("Cannot delete {name} because of"
                                  " foreign references").format(
                                      name=self.model._meta.verbose_name
                                  )
            messages.error(self.request, error_message)
            return HttpResponseRedirect(self.object.get_absolute_url())
        return result
