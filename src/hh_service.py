from abc import ABC
import requests
import json
import os


from src.main import Vacancies


class HeadHunterApi(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала Head Hunter
    """
    def __init__(self, keyword):
        self.keyword = keyword  # ключевое слово, по которому ведется поиск вакансии
        self.url = 'https://api.hh.ru/vacancies'  # адрес запроса вакансий

    def __len__(self):
        pass

    def get_vacancies(self):
        """
        Получаем список вакансий по запросу
        :return:
        """

        # формируем справочник для параметров GET-запроса
        params = {
            'text': self.keyword,  # Текст фильтра (ключевое слово)
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 10  # Кол-во вакансий на 1 странице
        }



        req = requests.get(self.url, params)  # Посылаем запрос к API
        data_in = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()

        data_out = json.loads(data_in)  # преобразуем полученные данные из формата json
        print(len(data_out))

        return data_out


test_1 = HeadHunterApi('python')
test_print = test_1.get_vacancies()
print(test_print)
for item in test_print['items']:
    print(item)
