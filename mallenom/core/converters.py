class RussianSlugConverter:
    """URL converter для поддержки кирилицы
    в адресной строке (необходима регистрация).
    """
    regex = '[-а-яА-Яa-zA-Z0-9_ёЁ]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
