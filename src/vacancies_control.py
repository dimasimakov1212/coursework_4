import json
from abc import ABC, abstractmethod
import os
# from src.main import general_function


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

    def vacancy_start_menu(self):
        """
        Создает диалог работы со списком полученных вакансий
        :return:
        """
        print("Полученный список вакансий можно отсортировать по зарплате и вывести топ вакансий на экран")
        top_list_num = int(input("Введите количество вакансий выводимых на экран\n"))
        choice_sort = int(input("Выберите вариант сортировки:\n"
                                "1 - по максимальной зарплате (иногда ее не указывают в вакансиях)\n"
                                "2 - по минимальной зарплате\n"))

        if choice_sort == 1:
            top_list = VacanciesControl.vacancy_sort_by_salary_to(self)
            VacanciesControl.print_top_to_screen(self, top_list, top_list_num)

        if choice_sort == 2:
            top_list = VacanciesControl.vacancy_sort_by_salary_from(self)
            VacanciesControl.print_top_to_screen(self, top_list, top_list_num)

    def print_top_to_screen(self, list_in, num_vacancy):
        """
        Выводит на экран топ вакансий
        :return:
        """
        for item in range(0, num_vacancy):
            print(f"{list_in[item]['name']}\n"
                  f"{list_in[item]['salary_from']} {list_in[item]['currency']}\n"
                  f"{list_in[item]['salary_to']} {list_in[item]['currency']}\n"
                  f"{list_in[item]['employer']}\n"
                  f"{list_in[item]['vacancy_url']}\n")

    def vacancy_sort_by_salary_to(self):
        """
        Сортирует вакансии по максимальной зарплате
        :return:
        """
        self.vacancies_all = sorted(self.vacancies_all, key=lambda k: k['salary_to'], reverse=True)
        return self.vacancies_all

    def vacancy_sort_by_salary_from(self):
        """
        Сортирует вакансии по минимальной зарплате
        :return:
        """
        self.vacancies_all = sorted(self.vacancies_all, key=lambda k: k['salary_from'], reverse=True)
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


# b = [{'salary_to': '500', 'id': 125}, {'salary_to': 0, 'id': 356}, {'salary_to': 200, 'id': 7854}]
# a = VacanciesControl(b)
# c = a.vacancy_sort_by_salary_to()
# print(c)
# a.write_to_file_menu()
