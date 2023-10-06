import re

import requests
from bs4 import BeautifulSoup

DEFINITION_COUNT = 20  # Количество определений для каждой найденной аббревиатуре

with open('text.txt', 'r', encoding='UTF-8') as text_file:
    abbreviation_list = re.findall(r'[A-ZА-ЯЁ]{2,}', text_file.read())

with open('abbreviations.txt', 'w', encoding='UTF-8') as abbreviation_file:
    for abbreviation in abbreviation_list:
        print(f'{abbreviation} - обработка...')
        site = requests.get(f'https://sokr.ru/{abbreviation}').text
        soup = BeautifulSoup(site, 'lxml')
        founded = soup.find_all('p', class_='value', limit=DEFINITION_COUNT)
        for i, request in enumerate(founded):
            abbreviation_file.write(
                f"{i+1}. {abbreviation if not i else ' ' * (len(abbreviation) - len(str(i + 1)) + 1)}"
                f" - {request.text}\n")
        abbreviation_file.write('\n')
