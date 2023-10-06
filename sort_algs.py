import random
import time


# Служебные декораторы функций
def __work_time(func):
    """Выводит на экран время работы функции, к которой применяется"""

    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'Время проверки = {end - start} секунд')
        print()
        return res

    return wrapper


def __put_line(line=''):
    """Просто вставляет строку после выполнения функции для красивого вывода"""

    def wrapper(func):

        def callable_(*args, **kwargs):
            res = func(*args, **kwargs)
            print(line)
            return res

        return callable_

    return wrapper


# Служебные функции
def __check_value(list_: list[int]):
    """Делает проверку списка"""
    if not isinstance(list_, list):
        raise TypeError('Функция принимает только список')
    try:
        sum(list_)
        if len(list_):
            range(list_[0])
    except TypeError:
        raise TypeError('Список должен состоять из целых чисел')


def __error_counter(true_sorted: list[int], to_check: list[int]) -> str:
    """Считает кол-во несовпадающих или совпадающих элементов списков true_sorted и to_check"""
    assert len(true_sorted) == len(to_check), 'Элементы списка утеряны'
    counter = 0
    for i in range(len(true_sorted)):
        if to_check[i] != true_sorted[i]:
            counter += 1
    counter = len(true_sorted) - counter  # Закомментировать, если необходимо количество ошибок
    return str(counter) + '/' + str(len(true_sorted))


@__work_time
def __print_results(sort_algorithm: callable, test_list: list[int]):
    true_sorted_test = sorted(test_list)
    print(f'+ {str(len(true_sorted_test))}/{str(len(true_sorted_test))}'
          if sort_algorithm(test_list) == true_sorted_test else
          f'- {__error_counter(true_sorted_test, test_list)}')


# Квадратичные алгоритмы сортировок с асимптотикой O(price^2)
def insertion_sort(list_: list[int]) -> list[int]:
    """Сортировка списка list методом вставки"""
    __check_value(list_)
    sub_list = [list_.pop(0)]
    for elem in list_:
        sub_list.append(elem)
        for i in range(len(sub_list) - 1, 0, -1):
            if sub_list[i] < sub_list[i - 1]:
                sub_list[i], sub_list[i - 1] = sub_list[i - 1], sub_list[i]
            else:
                break
    return sub_list


def selection_sort(list_: list[int]) -> list[int]:
    """Сортировка списка list методом выбора"""
    __check_value(list_)
    for i in range(len(list_) - 1):
        for j in range(i + 1, len(list_)):
            if list_[j] < list_[i]:
                list_[j], list_[i] = list_[i], list_[j]
    return list_


def bubble_sort(list_: list[int]) -> list[int]:
    """Сортировка списка list методом пузырька"""
    __check_value(list_)
    for length in range(len(list_) - 1, 0, -1):
        for i in range(length):
            if list_[i] > list_[i + 1]:
                list_[i], list_[i + 1] = list_[i + 1], list_[i]
    return list_


def counting_sort(list_: list[int]) -> list[int]:
    """Сортировка списка list методом подсчёта"""
    __check_value(list_)
    num_frequency = {i: list_.count(i) for i in range(min(list_), max(list_) + 1)}
    list_ = []
    for i in num_frequency:
        list_ += [i] * num_frequency[i]
    return list_


# Рекурсивные алгоритмы сортировок
def quick_sort(list_: list[int]) -> list[int]:
    r"""Сортировка списка list методом быстрой сортировки Тони Хоара
Асимптотика: W(2logN * price)"""
    __check_value(list_)
    if len(list_) <= 1:
        return list_
    barrier = [list_[0]]
    less_than_barrier = []
    more_than_barrier = []
    for i in range(1, len(list_)):
        if list_[i] < barrier[0]:
            less_than_barrier.append(list_[i])
        elif list_[i] > barrier[0]:
            more_than_barrier.append(list_[i])
        else:
            barrier.append(list_[i])
    list_ = quick_sort(less_than_barrier) + barrier + quick_sort(more_than_barrier)
    return list_


def merge_sort(list_: list[int]) -> list[int]:
    """Сортировка списка list методом быстрой сортировки слиянием
Асимптотика: O(2logN * price)"""
    __check_value(list_)
    if len(list_) <= 1:
        return list_
    first_part = list_[:len(list_) // 2]
    second_part = list_[len(list_) // 2:]
    first_part = merge_sort(first_part)
    second_part = merge_sort(second_part)
    list_ = []
    while first_part and second_part:
        if first_part[0] <= second_part[0]:
            list_.append(first_part.pop(0))
        else:
            list_.append(second_part.pop(0))
    list_.extend(first_part)
    list_.extend(second_part)
    return list_


@__put_line('=' * 60)
def test_the_sort(sort_algorithm: callable):
    """Набор простейших тест-кейсов для проверки работоспособности алгоритмов сортировки"""
    print(sort_algorithm.__doc__)

    tests = ([random.randint(-100, 100) for _ in range(10000)],
             [0] * 10,)

    for i, test_list in enumerate(tests):
        print(f'Unittest #{i + 1}: ', end='')
        __print_results(sort_algorithm, test_list)


def main():
    test_the_sort(insertion_sort)
    test_the_sort(selection_sort)
    test_the_sort(bubble_sort)
    test_the_sort(counting_sort)
    test_the_sort(quick_sort)
    test_the_sort(merge_sort)


if __name__ == '__main__':
    main()
    