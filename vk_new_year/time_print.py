from sys import stdout
from time import strftime, localtime


def tprint(*args, sep=' ', end='\n', file=stdout, flush=False):
    """Добавляет примитивный вывод времени для строки"""
    print(strftime('%d.%m %H:%M:%S', localtime()), end=' | ', file=file, flush=flush)
    print(*args, sep=sep, end=end, file=file, flush=flush)
