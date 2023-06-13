from abc import ABC

from src.main import Vacancies


class HeadHunterApi(Vacancies, ABC):
    """
    Класс реализует получение вакансий с портала Head Hunter
    """
    def get_vacancies(self):
        pass
