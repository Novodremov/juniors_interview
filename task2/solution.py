import csv

import requests
from bs4 import BeautifulSoup

NEXT_URL = '/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
BASE_URL = 'https://ru.wikipedia.org'

# Был вынужден применить синхронный подход в связи с тем, что ссылки
# на следующие страницы формируются неочевидным образом. Если использовать
# алфавитный указатель из таблицы, где указаны первые 2 буквы названий,
# потеряются статьи с некириллическими названиями (их тоже очень много).
# При очевидной пагинации можно было бы применить асинхронный подход
# (например, библиотеку aiohttp) и скрипт отрабатывал бы гораздо быстрее.
animal_data = {}
while True:
    response = requests.get(BASE_URL + NEXT_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    animals = soup.find('div', class_='mw-category-columns').find_all('a')
    for animal in animals:
        animal_data[animal.text[0]] = animal_data.get(animal.text[0], 0) + 1
        print(animal.text)
    if not (next := soup.find('a', string='Следующая страница')):
        break
    NEXT_URL = next['href']
print(animal_data)

with open('beasts.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for key, value in animal_data.items():
        writer.writerow([key, value])


# Не вижу, что можно покрывать тестами в рамках задачи, поскольку скрипт
# выполняет одну и ту же конкретную задачу при каждом запуске.
