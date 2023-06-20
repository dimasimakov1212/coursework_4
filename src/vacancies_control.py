import json
from abc import ABC, abstractmethod
import os


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
        self.file_data = os.path.abspath('../src/vacancies.json')

        # self.vacancy_id = self.vacancies_all['id']  # id вакансии
        # self.vacancy_name = self.vacancies_all['name']  # название вакансии
        # self.vacancy_salary_from = self.vacancies_all['salary_from']  # нижний предел зарплаты
        # self.vacancy_salary_to = self.vacancies_all['salary_to']  # верхний предел зарплаты
        # self.vacancy_currency = self.vacancies_all['currency']  # валюта зарплаты
        # self.vacancy_employer = self.vacancies_all['employer']  # наименование работодателя
        # self.vacancy_vacancy_url = self.vacancies_all['vacancy_url']  # ссылка на вакансию
        # self.vacancy_description = self.vacancies_all['description']  # описание вакансии
        # self.vacancy_experience = self.vacancies_all['experience']  # требуемый опыт работы

        # self.list_count += 1

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"{self.vacancies_all}"

    def __len__(self):
        return len(self.vacancies_all)

    # @classmethod
    def vacancy_sort_menu(self):
        """
        
        :return:
        """
        if self.vacancies_all != 0:
            print(self.vacancies_all)

    def vacancy_sort_by_salary_to(self):
        """
        Сортирует вакансии по максимальной зарплате
        :return:
        """
        self.vacancies_all = sorted(self.vacancies_all, key=lambda k: k['salary_to'], reverse=True)
        return self.vacancies_all

    def write_to_file_menu(self):
        """
        Записывает список вакансий в файл
        :return:
        """
        # проверяем пустой файл или нет
        try:
            if os.stat(self.file_data).st_size > 0:
                print("Файл содержит данные. Что необходимо сделать?:\n"
                      "1 - перезаписать данные\n"
                      "2 - добавить данные к существующим")
                file_action = int(input())

                # перезаписывает данные о вакансиях
                if file_action == 1:
                    VacanciesControl.writing_json(self)
                    print(f"Файл содержит {len(self.vacancies_all)} вакансий")

                # считывается содержимое файла и добавляется в список вакансий
                if file_action == 2:
                    data_1 = VacanciesControl.reading_json(self)
                    for item in data_1:
                        self.vacancies_all.append(item)

                    VacanciesControl.writing_json(self)
                    print(f"Файл содержит {len(self.vacancies_all)} вакансий")

            # если файл пустой записываем данные
            else:
                VacanciesControl.writing_json(self)
                print(f"Файл содержит {len(self.vacancies_all)} вакансий")

        except OSError:
            print("Файл не найден")

    def writing_json(self):
        """
        Записывает данные в формате json
        :return:
        """
        with open(self.file_data, 'w') as file:
            json.dump(self.vacancies_all, file, sort_keys=False, indent=4, ensure_ascii=False)

    def reading_json(self):
        """
        Считывает данные из формата json
        :return:
        """
        with open(self.file_data, 'r') as file:
            data_1 = json.load(file)
        return data_1


# b = [{'salary_to': 500, 'id': 125}, {'salary_to': 1000, 'id': 356}, {'salary_to': 200, 'id': 7854}]
# a = VacanciesControl(b)
# c = a.vacancy_sort_by_salary_to()
# print(c)
# a.write_to_file_menu()
