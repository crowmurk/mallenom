from logging import Filter

class ManagementFilter(Filter):
    def filter(self, record):
        """Фильтрует вывод лога
        """
        if hasattr(record, 'funcName') and record.funcName in [
                'execute',
                'tick',
                'watch_dir',
        ]:
            return False
        return True
