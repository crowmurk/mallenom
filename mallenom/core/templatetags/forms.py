from django.template import Library, TemplateSyntaxError

from core.templatetags.names import verbose_name

register = Library()

@register.inclusion_tag(
    'core/includes/filter_table_form.html',
    takes_context=True,
)
def filter_table_form(context, *args, **kwargs):
    """Тег представления filter form как таблицы
    """
    filter_form = (args[0] if len(args) > 0
                   else kwargs.get('filter'))

    if not filter_form:
        filter_form = context.get('filter')

    if filter_form is None:
        raise TemplateSyntaxError(
            "filter_table template tag requires "
            "at least one argument: filter.")

    return {
        'filter': filter_form,
    }


@register.inclusion_tag(
    'core/includes/action_table_form.html',
    takes_context=True,
)
def action_table_form(context, *args, **kwargs):
    """Тег формы таблицы с выбираемыми строками
    """
    request = context.get('request')

    table = (args[0] if len(args) > 0
             else kwargs.get('table'))

    if not table:
        table = context.get('table')

    if table is None:
        raise TemplateSyntaxError(
            "action_table template tag requires "
            "at least one argument: table.")

    object_type = kwargs.get('object_type')

    if object_type is None:
        model = getattr(table._meta, 'model', None)
        if model is None:
            object_type = 'objects'
        else:
            object_type = getattr(
                model._meta,
                'verbose_name_plural',
                'objects',
            )

    readonly = kwargs.get('readonly', False)
    action = kwargs.get('action', '')
    method = kwargs.get('method', 'post')
    button_type = kwargs.get('button_type', 'submit')
    button_class = kwargs.get('button_class', 'button')
    button_name = kwargs.get('button_name', 'action-table-button')
    button_value = kwargs.get('button_value', 'action-table-column-item')
    action_verbose = kwargs.get('action_verbose', 'Submit')

    return {
        'request': request,
        'table': table,
        'readonly': readonly,
        'action': action,
        'method': method,
        'button_type': button_type,
        'button_class': button_class,
        'button_name': button_name,
        'button_value': button_value,
        'action_verbose': action_verbose,
        'object_type': object_type,
    }


@register.inclusion_tag(
    'core/includes/formset_table.html',
    takes_context=True,
)
def formset_table(context, *args, **kwargs):
    """Тег представления formset как таблицы
    """
    request = context.get('request')

    formset = (args[0] if len(args) > 0
               else kwargs.get('formset'))

    if not formset:
        formset = context.get('formset')

    if formset is None:
        raise TemplateSyntaxError(
            "formset_table template tag requires "
            "at least one argument: formset.")

    paginator = (args[1] if len(args) > 1
                 else kwargs.get('paginator'))

    if not paginator:
        paginator = context.get('paginator')

    return {
        'request': request,
        'formset': formset,
        'paginator': paginator,
    }


@register.inclusion_tag(
    'core/includes/form.html',
    takes_context=True,
)
def form(context, *args, **kwargs):
    """Тег формы создания и изменения объекта.
    """
    request = context.get('request')

    action = (args[0] if len(args) > 0
              else kwargs.get('action'))

    if action is None:
        raise TemplateSyntaxError(
            "form template tag requires "
            "at least one argument: action, "
            "which is a URL.")

    action_verbose = (args[1] if len(args) > 1
                      else kwargs.get('action_verbose'))

    view = context.get('view')

    if hasattr(view, 'model'):
        action_verbose = ' '.join(
            [action_verbose,
             verbose_name(view.model).lower()],
        )

    method = (args[2] if len(args) > 2
              else kwargs.get('method'))

    display_object = kwargs.get('object', context.get('object'))

    cancel_url = kwargs.get(
        'cancel_url',
        display_object.get_absolute_url if display_object else None)

    form = context.get('form')
    formset = kwargs.get('formset', context.get('formset'))
    paginator = kwargs.get('paginator', context.get('paginator'))
    table = kwargs.get('table', context.get('table'))
    upload = kwargs.get('upload')

    return {
        'request': request,
        'action': action,
        'action_verbose': action_verbose,
        'method': method,
        'form': form,
        'object': display_object,
        'formset': formset,
        'paginator': paginator,
        'table': table,
        'upload': upload,
        'cancel_url': cancel_url,
    }


@register.inclusion_tag(
    'core/includes/delete_form.html',
    takes_context=True,
)
def delete_form(context, *args, **kwargs):
    """Тег формы удаления объекта.
    """
    action = (args[0] if len(args) > 0
              else kwargs.get('action'))

    if action is None:
        raise TemplateSyntaxError(
            "delete_form template tag "
            "requires at least one argument: "
            "action, which is a URL.")

    method = (args[1] if len(args) > 1
              else kwargs.get('method'))

    display_object = kwargs.get(
        'object', context.get('object'))

    if display_object is None:
        raise TemplateSyntaxError(
            "delete_form needs object "
            "manually specified in this case.")

    if hasattr(display_object, 'name'):
        object_name = display_object.name
    else:
        object_name = str(display_object)

    object_type = kwargs.get(
        'obj_type',
        verbose_name(display_object),
    )

    form = context.get('form')

    return {
        'action': action,
        'method': method,
        'object': display_object,
        'object_name': object_name,
        'object_type': object_type,
        'form': form,
    }
