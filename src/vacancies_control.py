from abc import ABC, abstractmethod


class Vacancies(ABC):
    """
    Абстрактный класс для поиска вакансий
    """
    @abstractmethod
    def get_vacancies(self):
        pass


class VacanciesControl:
    """
    Класс позволяет работать с полученными вакансиями
    """
    def __init__(self, vacancies_all):
        self.vacancies_all = vacancies_all

        pass
