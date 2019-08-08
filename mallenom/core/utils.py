from django.utils.text import slugify


def get_unique_slug(instance, slug_field, *args, **kwargs):
    """ Генерирует уникальный slug.
    Аргументы:
        instance - экземпляр модели
        slug_field - строка с именем поля в котором хранится slug
        args - источник для создания slug:
            строки с  именами полей экземпляра или
            строки значений для создания slug
        unique=True - должен ли slug быть уникальным или
        unique_for= () - строка или список строк с именами полей
            экземпляра с учетом которых slug должен быть уникальным
        prohibit = () - строка или  список строк запрещенных значений slug
    Возвращает:
        строку с уникальным slug
    """
    def tuple_from_kwarg(name, **kwargs):
        """Создает tuple из значения именованного аргумента.
        Значение должно быть строкой или списком строк.
        """
        value = kwargs.get(name, None)
        if value is None:
            return tuple()
        if isinstance(value, str):
            return (value, )
        if any([isinstance(value, item) for item in (list, tuple, set)]):
            if all([isinstance(item, str) for item in value]):
                return tuple(set(value))

        raise ValueError(
            "'{}' argument must be str or iterable of str.".format(name)
        )

    # Получаем значения полей экземпляра из которых создается slug
    if args and all([isinstance(arg, str) for arg in args]):
        source = [getattr(instance, arg, arg) for arg in args]
    else:
        raise ValueError("Slug source must be str or iterable of str.")

    # Составляем список запрещенных slug
    prohibit = ['create', 'update', 'delete']
    prohibit.extend(tuple_from_kwarg('prohibit', **kwargs))

    # Должен ли slug быть уникальным
    unique = kwargs.get('unique', True)
    unique_for = tuple_from_kwarg('unique_for', **kwargs)

    # Для уникальности будем создавать slug вида slug-1, slug-2, slug-n
    slugExtension = 1

    # Создаем slug
    slug = slugify(
        '-'.join([str(item) for item in source]),
        allow_unicode=True,
    )

    # Уникальность slug не требуется
    if not (unique or unique_for):
        if slug in prohibit:
            return "{}-{}".format(slug, slugExtension)
        return slug

    # Создаем уникальный slug
    if slug in prohibit:
        unique_slug = '{}-{}'.format(slug, slugExtension)
        slugExtension += 1
    else:
        unique_slug = slug

    # Формируем словарь для фильтра модели
    filter_dict = {slug_field: unique_slug}
    filter_dict.update(
        {field: getattr(instance, field) for field in unique_for}
    )

    # Пока slug не будет уникальным
    while instance.__class__.objects.filter(
        **filter_dict,
    ).exclude(id=instance.id).exists():
        # Генерируем новый slug
        unique_slug = '{}-{}'.format(slug, slugExtension)
        filter_dict.update({slug_field: unique_slug})
        slugExtension += 1

    return unique_slug
