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
        self.vacancies_list = []  # список, в который будут сохраняться вакансии по запросу
        # self.vacancy_id = None  # id вакансии
        # self.vacancy_name = None  # название вакансии
        # self.vacancy_salary_from = None  # нижний предел зарплаты
        # self.vacancy_salary_to = None  # верхний предел зарплаты
        # self.vacancy_url = None  # ссылка на вакансию
        # self.vacancy_description = None  # описание вакансии
        # self.vacancy_experience = None  # опыт работы

    def get_vacancies(self):
        """
        Формирует запрос на API сайта Head Hunter для получения выборки вакансий
        по ключевому слову
        :return: список вакансий по запросу
        """

        per_page_num = 2  # задаем кол-во вакансий на 1 странице
        page_num = 3  # задаем количество страниц

        # перебираем страницы с вакансиями
        for page in range(0, page_num):

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

            # vacancy_dict = {}  # словарь для данных о вакансии

            # полученные вакансии складываем в словарь и добавляем его в список
            for vacancy in data_out['items']:

                # запускаем метод формирования словаря
                vacancy_dict = HeadHunterApi.get_vacancy_dict(self, vacancy)

                # vacancy_dict['id'] = vacancy['id']  # id вакансии
                # vacancy_dict['name'] = vacancy['name']  # название вакансии
                # if vacancy['salary']:
                #     vacancy_dict['salary_from'] = vacancy['salary']['from']  # нижний предел зарплаты
                #     vacancy_dict['salary_to'] = vacancy['salary']['to']  # верхний предел зарплаты
                # else:
                #     vacancy_dict['salary_from'] = None
                #     vacancy_dict['salary_to'] = None
                # vacancy_dict['vacancy_url'] = vacancy['alternate_url']  # ссылка на вакансию
                # vacancy_dict['description'] = vacancy['snippet']['responsibility']  # описание вакансии
                # vacancy_dict['experience'] = vacancy['experience']['name']  # требуемый опыт работы

                # print(vacancy)
                self.vacancies_list.append(vacancy_dict)  # полученный словарь добавляем в список

            time.sleep(0.25)  # временная задержка во избежание блокировки большого количества запросов

        return self.vacancies_list

    def get_vacancy_dict(self, vacancy):
        """
        Формирует словарь с необходимыми данными о вакансии из словаря, полученного по API
        :return:
        """
        vacancy_dict = {}  # словарь для данных о вакансии

        vacancy_dict['id'] = vacancy['id']  # id вакансии
        vacancy_dict['name'] = vacancy['name']  # название вакансии
        if vacancy['salary']:
            vacancy_dict['salary_from'] = vacancy['salary']['from']  # нижний предел зарплаты
            vacancy_dict['salary_to'] = vacancy['salary']['to']  # верхний предел зарплаты
        else:
            vacancy_dict['salary_from'] = None
            vacancy_dict['salary_to'] = None
        vacancy_dict['vacancy_url'] = vacancy['alternate_url']  # ссылка на вакансию
        vacancy_dict['description'] = vacancy['snippet']['responsibility']  # описание вакансии
        vacancy_dict['experience'] = vacancy['experience']['name']  # требуемый опыт работы

        return vacancy_dict


test_1 = HeadHunterApi('python')
test_print = test_1.get_vacancies()
# print(test_1.vacancies_list)
for item in test_1.vacancies_list:
    print(item)

# print(test_print['items'][0])  # весь словарь
# print(test_print['items'][0]['id'])  # id вакансии
# print(test_print['items'][0]['name'])  # название вакансии
# print(test_print['items'][0]['salary']['from'])  # зарплата от
# print(test_print['items'][0]['salary']['to'])  # зарплата до
# print(test_print['items'][0]['alternate_url'])  # ссылка на вакансию
# print(test_print['items'][0]['snippet']['responsibility'])  # описание вакансии
# print(test_print['items'][0]['experience']['name'])  # опыт работы
