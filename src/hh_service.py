from abc import ABC
import requests
import json
import os
import time


from src.main import Vacancies


class HeadHunterApi(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала Head Hunter
    """
    def __init__(self, keyword):
        self.keyword = keyword  # ключевое слово, по которому ведется поиск вакансии
        self.url_api = 'https://api.hh.ru/vacancies'  # адрес запроса вакансий через API
        self.page_num = 0
        self.vacancies_list = []

    def get_vacancies(self):
        """
        Получаем список вакансий по запросу
        :return:
        """

        per_page_num = 2  # задаем кол-во вакансий на 1 странице

        for page in range(0, 3):

            # формируем справочник для параметров GET-запроса
            params = {
                'text': self.keyword,  # Текст фильтра (ключевое слово)
                'area': 1,  # Поиск ощуществляется по вакансиям города Москва
                'page': page,  # Индекс страницы поиска на HH
                'per_page': per_page_num  # Кол-во вакансий на 1 странице
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                              "Safari/537.36",  # Replace with your User-Agent header
            }

            # req = requests.get(self.url, params)  # Посылаем запрос к API без headers

            req = requests.get(self.url_api, params, headers=headers)  # Посылаем запрос к API
            data_in = req.content.decode()  # Декодируем ответ API, чтобы Кириллица отображалась корректно
            req.close()

            data_out = json.loads(data_in)  # преобразуем полученные данные из формата json

            # полученные вакансии складываем в список
            for vacancy in data_out['items']:

                # vacancy_list = vacancy[0]

                print(vacancy)
            #
            #     # self.vacancies_list.append(vacancy_list)

            time.sleep(0.25)

        return None

    # def get_page_vacancies(self):
    #     """
    #     Получает страницу с вакансиями
    #     :return:
    #     """
    #
    #
    #
    #     return data_out


test_1 = HeadHunterApi('python')
test_print = test_1.get_vacancies()
# print(test_print)
# for item in test_print['items']:
#     print(item)
# print(test_print['items'][0])  # весь словарь
# print(test_print['items'][0]['id'])  # id вакансии
# print(test_print['items'][0]['name'])  # название вакансии
# print(test_print['items'][0]['salary']['from'])  # зарплата от
# print(test_print['items'][0]['salary']['to'])  # зарплата от
# print(test_print['items'][0]['alternate_url'])  # ссылка на вакансию
# print(test_print['items'][0]['snippet']['responsibility'])  # описание вакансии
# print(test_print['items'][0]['experience']['name'])  # опыт работы
