from abc import ABC
import requests
import json
import time

from src.vacancies_control import Vacancies


class HeadHunterApi(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала HeadHunter
    """
    def __init__(self, keyword):
        self.keyword = keyword  # ключевое слово, по которому ведется поиск вакансии
        self.url_api = 'https://api.hh.ru/vacancies'  # адрес запроса вакансий через API
        self.vacancies_list = []  # список, в который будут сохраняться вакансии по запросу

    def __repr__(self):
        return f"{self.__class__.__name__}," \
               f"{self.keyword}," \
               f"{self.url_api}," \
               f"{self.vacancies_list}"

    def get_vacancies(self):
        """
        Формирует запрос на API сайта HeadHunter для получения выборки вакансий
        по ключевому слову
        :return: список вакансий по запросу
        """

        per_page_num = 100  # задаем кол-во вакансий на 1 странице
        page_num = 10  # задаем количество страниц
        vacancies_count = 0  # задаем счетчик вакансий

        # перебираем страницы с вакансиями
        for page in range(0, page_num):

            # формируем справочник для параметров GET-запроса
            params = {
                'text': self.keyword,  # Текст фильтра (ключевое слово)
                # 'area': 1,  # Поиск ощуществляется по вакансиям города Москва
                'page': page,  # Индекс страницы поиска на HH
                'per_page': per_page_num  # Кол-во вакансий на 1 странице
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 "
                              "Safari/537.36",
            }

            req = requests.get(self.url_api, params=params, headers=headers)  # Посылаем запрос к API

            if req.status_code == 200:  # проверяем на корректность ответа

                data_in = req.content.decode()  # Декодируем ответ API, чтобы Кириллица отображалась корректно
                req.close()

                data_out = json.loads(data_in)  # преобразуем полученные данные из формата json

                # полученные вакансии складываем в словарь и добавляем его в список
                for vacancy in data_out['items']:

                    # запускаем метод формирования словаря
                    vacancy_dict = HeadHunterApi.get_vacancy_dict(vacancy)

                    self.vacancies_list.append(vacancy_dict)  # полученный словарь добавляем в список
                    vacancies_count += 1  # увеличиваем счетчик вакансий

            if req.status_code != 200:
                print("В настоящий момент сайт недоступен. Попробуйте позже.")

            if vacancies_count == data_out['found']:  # проверка на наличие вакансий на странице
                break

            time.sleep(0.2)  # временная задержка во избежание блокировки большого количества запросов

        return self.vacancies_list

    @classmethod
    def get_vacancy_dict(cls, vacancy):
        """
        Формирует словарь с необходимыми данными о вакансии из словаря, полученного по API
        :return:
        """
        vacancy_dict = {}  # словарь для данных о вакансии

        vacancy_dict['id'] = int(vacancy['id'])  # id вакансии
        vacancy_dict['name'] = vacancy['name']  # название вакансии
        if vacancy['salary']:
            if vacancy['salary']['from'] is None:  # проверяем наличие данных
                vacancy_dict['salary_from'] = 0
            else:
                vacancy_dict['salary_from'] = vacancy['salary']['from']  # нижний предел зарплаты

            if vacancy['salary']['to'] is None:  # проверяем наличие данных
                vacancy_dict['salary_to'] = 0
            else:
                vacancy_dict['salary_to'] = vacancy['salary']['to']  # верхний предел зарплаты

            if vacancy['salary']['currency'] is None:  # проверяем наличие данных
                vacancy_dict['currency'] = 'RUR'
            else:
                vacancy_dict['currency'] = vacancy['salary']['currency']  # валюта зарплаты
        else:
            vacancy_dict['salary_from'] = 0
            vacancy_dict['salary_to'] = 0
            vacancy_dict['currency'] = 'RUR'
        vacancy_dict['employer'] = vacancy['employer']['name']  # наименование работодателя
        vacancy_dict['vacancy_url'] = vacancy['alternate_url']  # ссылка на вакансию
        vacancy_dict['description'] = vacancy['snippet']['responsibility']  # описание вакансии
        vacancy_dict['experience'] = vacancy['experience']['name']  # требуемый опыт работы

        return vacancy_dict


# test_1 = HeadHunterApi('python')
# test_1.get_vacancies()
# a = test_1.vacancies_list
#
# for item in test_1.vacancies_list:
#     print(item)
