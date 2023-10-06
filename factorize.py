from functools import lru_cache
from time import time


# Кэширование функций для ускорения работы
@lru_cache(None)
def is_prime(num) -> bool:
    """Возвращает True, если данное число простое, и False, если число составное"""
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True
    # return all(num % i != 0 for i in range(2, int(num**0.5)+1))


@lru_cache(None)
def get_primes(num) -> list:
    """Возвращает список простых чисел до заданного числа (включительно)"""
    sub_list = []
    for j in range(2, num + 1):
        if is_prime(j):
            sub_list.append(j)
    return sub_list


def factorize(num) -> str:
    """Возвращает строку, состоящую из простых множителей числа и знаков умножения между ними"""
    result = ''
    # Частный случай для простых чисел
    if is_prime(num):
        return str(num) + '*1'
    # Общий случай для составных чисел
    while not is_prime(num):
        for div in get_primes(num):
            if num % div == 0:
                result += str(div) + '*'
                num //= div
    return result + str(num)


def main():
    for n in range(1000, 1000000):
        print(f'{n} = {factorize(n)}')
    # print(factorize(100000000))


if __name__ == '__main__':
    start_time = time()
    main()
    end_time = time()
    print(f'Время работы программы: {round(end_time-start_time, 2)} сек.')
