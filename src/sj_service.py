# Параметры доступа
# ID	2604
# Secret key	v3.r.137614806.f1965cb543def5c60782496be7a7ebc821b88608.5aaca3901c30bd49f51e0eebff148e7a02ac878d

from abc import ABC
import requests
import json
import os
import time


from src.main import Vacancies


class SuperJobAPI(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала Superjob
    """
    def __init__(self, keyword):
        self.keyword = keyword  # ключевое слово, по которому ведется поиск вакансии
        self.url_api = 'https://api.superjob.ru/2.0/vacancies'  # адрес запроса вакансий через API
        self.vacancies_list = []  # список, в который будут сохраняться вакансии по запросу
        self.s_key = "v3.r.137614806.f1965cb543def5c60782496be7a7ebc821b88608.5aaca3901c30bd49f51e0eebff148e7a02ac878d"

    def get_vacancies(self):
        """
        Формирует запрос на API сайта Head Hunter для получения выборки вакансий
        по ключевому слову
        :return: список вакансий по запросу
        """
        per_page_num = 2  # задаем кол-во вакансий на 1 странице
        page_num = 2  # задаем количество страниц

        # перебираем страницы с вакансиями
        for page in range(0, page_num):

            headers = {"X-Api-App-Id": self.s_key}
            params = {'count': per_page_num, 'page': page, 'keyword': self.keyword, 'archive': False}

            response = requests.get(self.url_api, params=params, headers=headers)  # Посылаем запрос к API

            if response.status_code == 200:  # проверяем на корректность ответа

                data_in = response.content.decode()  # Декодируем ответ API, чтобы Кириллица отображалась корректно
                response.close()

                data_out = json.loads(data_in)  # преобразуем полученные данные из формата json

                for item in data_out['objects']:
                    print(item)

    @classmethod
    def get_vacancy_dict(cls, vacancy):
        """
        Формирует словарь с необходимыми данными о вакансии из словаря, полученного по API
        :return:
        """
        vacancy_dict = {}  # словарь для данных о вакансии

        vacancy_dict['id'] = vacancy['id']  # id вакансии
        vacancy_dict['name'] = vacancy['profession']  # название вакансии
        vacancy_dict['salary_from'] = vacancy['payment_from']  # нижний предел зарплаты
        vacancy_dict['salary_to'] = vacancy['payment_to']  # верхний предел зарплаты
        vacancy_dict['vacancy_url'] = vacancy['link']  # ссылка на вакансию
        vacancy_dict['description'] = vacancy['vacancyRichText']  # описание вакансии
        vacancy_dict['experience'] = vacancy['experience']['title']  # требуемый опыт работы

        return vacancy_dict


test_1 = SuperJobAPI('python')
test_print = test_1.get_vacancies()
