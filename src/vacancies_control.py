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
    list_count = 0

    def __init__(self, vacancies_all):
        self.vacancies_all = vacancies_all

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"{self.vacancies_all}"

    def __len__(self):
        return len(self.vacancies_all)

