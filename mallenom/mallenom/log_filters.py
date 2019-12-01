from logging import Filter

class ManagementFilter(Filter):
    """Добавляет фильтр для лога.
    """
    def filter(self, record):
        """Фильтрует вывод в лог.
        """
        if hasattr(record, 'funcName') and record.funcName in [
                'execute',
                'tick',
                'watch_dir',
        ]:
            return False
        return True
