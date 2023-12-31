# Параметры доступа
# ID	2604
# Secret key	v3.r.137614806.f1965cb543def5c60782496be7a7ebc821b88608.5aaca3901c30bd49f51e0eebff148e7a02ac878d

from abc import ABC
import requests
import json
import os
import time


from src.vacancies_control import Vacancies


class SuperJobAPI(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала Superjob
    """
    def __init__(self, keyword):
        self.keyword = keyword  # ключевое слово, по которому ведется поиск вакансии
        self.url_api = 'https://api.superjob.ru/2.0/vacancies'  # адрес запроса вакансий через API
        self.vacancies_list = []  # список, в который будут сохраняться вакансии по запросу

    def __repr__(self):
        return f"{self.__class__.__name__}," \
               f"{self.keyword}," \
               f"{self.url_api}," \
               f"{self.vacancies_list}"

    def get_vacancies(self):
        """
        Формирует запрос на API сайта Head Hunter для получения выборки вакансий
        по ключевому слову
        :return: список вакансий по запросу
        """

        per_page_num = 100  # задаем кол-во вакансий на 1 странице
        page_num = 5  # задаем количество страниц
        api_key: str = os.getenv('SJ_API_KEY')  # получаем ключ API
        vacancies_count = 0  # задаем счетчик вакансий

        # перебираем страницы с вакансиями
        for page in range(0, page_num):

            # передаем секретный ключ для API клиента
            headers = {"X-Api-App-Id": api_key}
            # формируем справочник для параметров GET-запроса
            params = {'count': per_page_num, 'page': page, 'keyword': self.keyword, 'archive': False}

            response = requests.get(self.url_api, params=params, headers=headers)  # Посылаем запрос к API

            if response.status_code == 200:  # проверяем на корректность ответа

                data_in = response.content.decode()  # Декодируем ответ API, чтобы Кириллица отображалась корректно
                response.close()

                data_out = json.loads(data_in)  # преобразуем полученные данные из формата json

                # полученные вакансии складываем в словарь и добавляем его в список
                for vacancy in data_out['objects']:
                    # запускаем метод формирования словаря
                    vacancy_dict = SuperJobAPI.get_vacancy_dict(vacancy)

                    self.vacancies_list.append(vacancy_dict)  # полученный словарь добавляем в список

                    vacancies_count += 1  # увеличиваем счетчик вакансий

            if response.status_code != 200:
                print("В настоящий момент сайт недоступен. Попробуйте позже.")

            if vacancies_count == data_out['total']:  # проверка на наличие вакансий
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

        vacancy_dict['id'] = vacancy['id']  # id вакансии
        vacancy_dict['name'] = vacancy['profession']  # название вакансии
        vacancy_dict['salary_from'] = vacancy['payment_from']  # нижний предел зарплаты
        vacancy_dict['salary_to'] = vacancy['payment_to']  # верхний предел зарплаты
        vacancy_dict['currency'] = vacancy['currency']  # валюта зарплаты
        try:
            vacancy_dict['employer'] = vacancy['client']['title']  # наименование работодателя
        except KeyError:
            vacancy_dict['employer'] = 'Нет данных'
        vacancy_dict['vacancy_url'] = vacancy['link']  # ссылка на вакансию
        vacancy_dict['description'] = vacancy['vacancyRichText']  # описание вакансии
        vacancy_dict['experience'] = vacancy['experience']['title']  # требуемый опыт работы

        return vacancy_dict


# test_1 = SuperJobAPI('python')
# test_print = test_1.get_vacancies()
#
# for item in test_1.vacancies_list:
#     print(item)
