import random
import sys
from datetime import date, datetime
from os import system
from time import sleep

import requests
import vk_api
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

from time_print import tprint
from config import *

MAX_TRIES = 10

system('cls')
init(autoreset=True)
session = vk_api.VkApi(token=VK_TOKEN)
vk = session.get_api()


def get_kitties(owner_id=-215379409, album_id='wall', token=VK_TOKEN):
    """Возвращает список фотографий в альбоме милых всратышей"""
    try:
        return vk.photos.get(access_token=token, owner_id=owner_id, album_id=album_id)
    except vk_api.exceptions.ApiError or vk_api.exceptions.ApiHttpError as err:
        tprint(f'{Fore.RED}Ошибка {Back.WHITE}"{err}"{Style.RESET_ALL}')
        tprint(f'{Fore.RED}Программа ушла в режим ожидания на {Back.WHITE}10 минут{Style.RESET_ALL}')
        sleep(600)


def post(message, token=VK_TOKEN, owner_id=-217158177, attachment=None):
    """Создаёт пост в соответствии с заданными параметрами"""
    try:
        vk.wall.post(access_token=token, message=message, owner_id=owner_id, from_group=1, attachment=attachment)
        tprint(f'{Fore.GREEN}Новый пост: {message or "<empty message>"}{Style.RESET_ALL}')
    except vk_api.exceptions.ApiError or vk_api.exceptions.ApiHttpError as err:
        tprint(f'{Fore.RED}Ошибка {Back.WHITE}"{err}"{Style.RESET_ALL}')
        tprint(f'{Fore.RED}Программа ушла в режим ожидания на {Back.WHITE}10 минут{Style.RESET_ALL}')
        sleep(600)


def get_days_to_new_year(someday=None):
    """Возвращает количество дней от заданной даты до следующего Нового Года"""
    if someday is None:
        someday = date.today()
    new_year = date(someday.year + 1, 1, 1)
    return (new_year - someday).days if (new_year - someday).days < 365 else 0


def get_object_form(object_count):
    """Возвращает слово 'день' в правильной форме в зависимости от количества"""
    if object_count == 1:
        return 'день'
    if object_count < 5:
        return 'дня'
    return 'дней'


def get_daily_fact():
    """Возвращает факт дня (https://dailyfacts.org/) на английском языке"""
    try:
        fact_html = requests.get('https://dailyfacts.org/').text
        soup = BeautifulSoup(fact_html, 'html.parser')
        try:
            result = soup.find('div', class_='fact-content').text
        except AttributeError as err:
            result = '<ошибка получения факта, сегодня без него :(>'
            tprint(f'{Fore.RED}Ошибка {Back.WHITE}{err}{Style.RESET_ALL}')
    except requests.exceptions.ConnectionError as err:
        result = '<ошибка получения факта, сегодня без него :(>'
        tprint(f'{Fore.RED}Ошибка {Back.WHITE}{err}{Style.RESET_ALL}')
    return result.strip()


def microsoft_translate(text):
    """Использует Microsoft Translate в качестве переводчика и возвращает переданный текст на русском языке"""
    url = 'https://microsoft-translator-text.p.rapidapi.com/translate'
    payload = [{'Text': text}]
    querystring = {'to[0]': 'ru', 'api-version': '3.0', 'profanityAction': 'NoAction', 'textType': 'plain'}
    # noinspection SpellCheckingInspection
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': 'e468ef6007msh61d4bb92cdce3abp129bffjsn83d2c602737a',
        'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    }
    try:
        return requests.post(url, json=payload, headers=headers, params=querystring).json()[0]['translations'][0]['text']
    except KeyError:
        return '<ошибка на стадии перевода>'


def deep_translate(text):
    url = 'https://deep-translate1.p.rapidapi.com/language/translate/v2'
    payload = {
        'q': text,
        'source': 'en',
        'target': 'ru'
    }
    # noinspection SpellCheckingInspection
    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': 'e468ef6007msh61d4bb92cdce3abp129bffjsn83d2c602737a',
        'X-RapidAPI-Host': 'deep-translate1.p.rapidapi.com'
    }
    try:
        return requests.post(url, json=payload, headers=headers).json()['data']['translations']['translatedText']
    except KeyError:
        return '<ошибка на стадии перевода>'


def main():     # Я из будущего. Это использование main неправильное
    days = get_days_to_new_year()
    if days:  # Если функция вернёт число > 0
        daily_fact = get_daily_fact()
        kitties_ids = []
        for item in get_kitties()['items']:
            kitties_ids.append(f'photo-215379409_{item["id"]}')
        post(f'Нет. :(\n'
             f'Новый Год только через {days} {get_object_form(days)}.\n'
             f'Интересный факт на сегодня, чтобы не скучать: \n'
             f'{deep_translate(daily_fact) if daily_fact != "<ошибка получения факта, сегодня без него :(>" else ""}\n'
             f'({daily_fact})\n'
             f'P.S. Перевод автоматический, возможны ошибки и неточности',
             attachment=random.choice(kitties_ids))
    else:  # Если функция вернёт 0
        post(f'ДА!\nСегодня Новый Год, с праздником!\n')


def flow_control():
    """Функция поддержки программы 'на плаву' в случае разрыва соединения"""
    while True:
        try:
            main()
            tprint('Программа успешно проработала сегодня, до встречи через 24 часа!')
            sleep(86400)  # 60*60*24 секунд
        except requests.exceptions.ConnectionError as err:
            tprint(f'{Fore.RED}Ошибка {Back.WHITE}{err}{Back.RESET}, '
                   f'перевод в режим ожидания на 10 минут{Style.RESET_ALL}')
            sleep(600)


if __name__ == '__main__':
    # if sys.argv[1:]:
    #     flow_control()
    # else:
    #     print(f'{Fore.RED}(!){Back.WHITE}ЛОЖНОЕ СРАБАТЫВАНИЕ ИЛИ ЗАПУСК БЕЗ АРГУМЕНТОВ{Back.RESET}(!){Style.RESET_ALL}')
    while True:
        now = datetime.now()
        if now.hour == 8:
            if now.minute == 0:
                break
        tprint()
        sleep(5)
    flow_control()

