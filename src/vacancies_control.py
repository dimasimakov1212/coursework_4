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

    def __init__(self, vacancies_all):
        self.vacancies_all = vacancies_all  # список вакансий
        self.file_data = os.path.abspath('./src/vacancies.json')  # файл для хранения списка вакансий

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
        top_list_num = int(input("Введите количество вакансий выводимых на экран:\n"))

        if 0 < top_list_num <= len(self.vacancies_all):
            choice_sort = int(input("Выберите вариант сортировки:\n"
                                    "1 - по максимальной зарплате (если параметр не задан, будет указан 0)\n"
                                    "2 - по минимальной зарплате (если параметр не задан, будет указан 0)\n"
                                    "-------------------------------------\n"))

            if choice_sort == 1:
                # запрашиваем вариант вывода топа вакансий
                choice_record = VacanciesControl.choice_to_record_top_vacancies()
                # получаем сортированный список вакансий по максимальной зарплате
                top_list = VacanciesControl.vacancy_sort_by_salary_to(self)
                # осуществляем вывод на экран и запись вакансий в файл
                VacanciesControl.actions_for_top_vacancies(self, top_list, choice_record, top_list_num)

            if choice_sort == 2:
                # запрашиваем вариант вывода топа вакансий
                choice_record = VacanciesControl.choice_to_record_top_vacancies()
                # получаем сортированный список вакансий по минимальной зарплате
                top_list = VacanciesControl.vacancy_sort_by_salary_from(self)
                # осуществляем вывод на экран и запись вакансий в файл
                VacanciesControl.actions_for_top_vacancies(self, top_list, choice_record, top_list_num)

        else:
            print("Введено неправильное количество вакансий, выводимых в топ")

    def actions_for_top_vacancies(self, top_list, top_list_action, top_list_num):
        """
        Осуществляет вывод на экран и запись вакансий в зависимости от выбора пользователя
        :param top_list_num: количество выводимых в топ вакансий
        :param top_list: топ вакансий список
        :param top_list_action: выбор действий
        :return:
        """
        # вывод на экран и запись в файл
        if top_list_action == 1:
            self.vacancies_all = []  # очищаем список вакансий оъект класса
            for item in range(0, top_list_num):
                VacanciesControl.print_to_screen(self, top_list[item])  # выводим топ вакансий на экран
                self.vacancies_all.append(top_list[item])  # записываем список топ вакансий

            VacanciesControl.write_to_file_menu(self)  # запускаем меню записи вакансий в файл

        # вывод на экран без записи в файл
        if top_list_action == 2:
            for item in range(0, top_list_num):
                VacanciesControl.print_to_screen(self, top_list[item])  # выводим топ вакансий на экран

    @classmethod
    def choice_to_record_top_vacancies(cls):
        """
        Диалог записи в файл выведенных в топ вакансий
        """
        choice_record = int(input("Записать выбранные вакансии в файл?\n"
                                  "1 - вывести на экран и записать\n"
                                  "2 - вывести на экран (не записывать)\n"))
        return choice_record

    def print_to_screen(self, list_in):
        """
        Выводит на экран топ вакансий
        """
        print(f"ID вакансии: {list_in['id']}\n"
              f"Вакансия: {list_in['name']}\n"
              f"Минимальная зарплата: {list_in['salary_from']} {list_in['currency']}\n"
              f"Максимальная зарплата: {list_in['salary_to']} {list_in['currency']}\n"
              f"Наименование работодателя: {list_in['employer']}\n"
              f"Ссылка на вакансию: {list_in['vacancy_url']}\n")

    def vacancy_sort_by_salary_to(self):
        """
        Сортирует вакансии по максимальной зарплате
        :return: сортированный список
        """
        self.vacancies_all = sorted(self.vacancies_all, key=lambda k: k['salary_to'], reverse=True)
        return self.vacancies_all

    def vacancy_sort_by_salary_from(self):
        """
        Сортирует вакансии по минимальной зарплате
        :return: сортированный список
        """
        self.vacancies_all = sorted(self.vacancies_all, key=lambda k: k['salary_from'], reverse=True)
        return self.vacancies_all

    def write_to_file_menu(self):
        """
        Записывает список вакансий в файл
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

                # считывается содержимое файла и добавляется в список вакансий
                if file_action == 2:
                    data_1 = VacanciesControl.reading_json(self)
                    for item in data_1:
                        self.vacancies_all.append(item)

                    VacanciesControl.writing_json(self)  # записывается дополненный список в файл

            # если файл пустой записываем данные
            else:
                VacanciesControl.writing_json(self)

        except OSError:
            print("Файл не найден")

    def writing_json(self):
        """
        Записывает данные в формате json
        """
        with open(self.file_data, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies_all, file, sort_keys=False, indent=4, ensure_ascii=False)

        print(f"Файл содержит {len(self.vacancies_all)} вакансий")

    def reading_json(self):
        """
        Считывает данные из формата json
        :return: список вакансий
        """
        with open(self.file_data, 'r', encoding='utf-8') as file:
            data_1 = json.load(file)
        return data_1

    def sort_vacancies_menu(self):
        """
        Запускает диалог по сортировке вакансий, сохраненных в файле
        """
        print("Список вакансий можно отредактировать, удалив ненужные по их ID\n"
              "После этого можно запустить новый поиск и добавить новые вакансии в файл\n"
              "-------------------------------------\n")

        # выводим вакансии на экран
        for item in range(0, len(self.vacancies_all)):
            VacanciesControl.print_to_screen(self, self.vacancies_all[item])

        id_to_delete = int(input("Введите ID вакансии, которую необходимо удалить:\n"))

        # удалаем вакансию по ID
        VacanciesControl.delete_vacancy_by_id(self, id_to_delete)
        # записываем обновленный список вакансий
        VacanciesControl.writing_json(self)

    def delete_vacancy_by_id(self, vacancy_id):
        """
        Удаляет из списка вакансию по выбранному ID
        :param vacancy_id:
        :return: обновленный список вакансий
        """
        list_to_sort = self.vacancies_all  # копируем первоначальный список вакансий
        self.vacancies_all = []  # обнуляем первоначальный список

        # проверяется id вакансии, если соответствует заданному, то пропускается
        # остальные вакансии складываются в список
        for item in list_to_sort:
            if item['id'] != vacancy_id:
                self.vacancies_all.append(item)

        return self.vacancies_all


# b = [{'salary_to': 500, 'id': 125}, {'salary_to': 0, 'id': 356}, {'salary_to': 200, 'id': 7854}]
# a = VacanciesControl(b)
# print(a.vacancies_all)
# c = a.vacancy_sort_by_salary_to()
# print(c)
# VacanciesControl.writing_json(a)
