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
