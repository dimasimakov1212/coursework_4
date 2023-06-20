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

        # self.vacancy_id = self.vacancies_all['id']  # id вакансии
        # self.vacancy_name = self.vacancies_all['name']  # название вакансии
        # self.vacancy_salary_from = self.vacancies_all['salary_from']  # нижний предел зарплаты
        # self.vacancy_salary_to = self.vacancies_all['salary_to']  # верхний предел зарплаты
        # self.vacancy_currency = self.vacancies_all['currency']  # валюта зарплаты
        # self.vacancy_employer = self.vacancies_all['employer']  # наименование работодателя
        # self.vacancy_vacancy_url = self.vacancies_all['vacancy_url']  # ссылка на вакансию
        # self.vacancy_description = self.vacancies_all['description']  # описание вакансии
        # self.vacancy_experience = self.vacancies_all['experience']  # требуемый опыт работы

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"{self.vacancies_all}"

    def __len__(self):
        return len(self.vacancies_all)

    def vacancy_sort_by_salary_to(self):
        """
        Сортирует вакансии по максимальной зарплате
        :return:
        """
        self.vacancies_all = sorted(self.vacancies_all, key=lambda k: k['salary_to'], reverse=True)
        return self.vacancies_all


b = [{'salary_to': 500, 'id': 125}, {'salary_to': 1000, 'id': 356}, {'salary_to': 200, 'id': 7854}]
a = VacanciesControl(b)
c = a.vacancy_sort_by_salary_to()
print(c)
