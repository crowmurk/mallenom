from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

class ActionTableDeleteMixin:
    action_table_model = None
    action_table_button = "action-table-button"
    action_table_success_message = None
    action_table_multitables = None

    def post(self, request, *args, **kwargs):
        if self.action_table_model:
            self.action_table_multitables = [
                {
                    'model': self.action_table_model,
                    'button': self.action_table_button,
                    'success_message': self.action_table_success_message,
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
            success_message = action_table['success_message']

            button = request.POST.get(button)
            pks = request.POST.getlist(button)
            if pks:
                selected_objects = model.objects.filter(pk__in=pks)
                selected_objects.delete()
                if success_message:
                    messages.success(self.request, success_message)

        return HttpResponseRedirect(request.path)


class SuccessDeleteMessageMixin:
    success_message = None

    def delete(self, request, *args, **kwargs):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
