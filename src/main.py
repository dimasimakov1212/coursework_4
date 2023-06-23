from src.hh_service import HeadHunterApi
from src.sj_service import SuperJobAPI
from src.vacancies_control import VacanciesControl
import json
import os


file_in = os.path.abspath('./src/vacancies.json')


def general_function(check_point):
    """
    Запускает основное тело программы
    :return:
    """
    if check_point:
        start_menu()


def start_menu():
    """
    Стартовое меню навигации по программе
    :return:
    """

    print("-------------------------------------")
    print("Выберите необходимое действие:\n")
    start_point = int(input("1 - запуск поиска вакансий и сортировка списка\n"
                            "2 - редактирование списка вакансий\n"
                            "4 - выход из программы\n"))

    if start_point == 1:
        list_in = choice_vacancies_portal()
        list_out = VacanciesControl(list_in)
        VacanciesControl.vacancy_start_menu(list_out)
        general_function(True)

    if start_point == 2:
        list_in = reading_json_file(file_in)
        list_for_sort = VacanciesControl(list_in)
        list_for_sort.sort_vacancies_menu()

        general_function(True)

    if start_point == 4:
        end_program()


def choice_vacancies_portal():
    """
    Позволяет выбрать портал для поиска вакансий и задать поисковый запрос
    :return:
    """
    choice_portal = int(input("Выберите место поиска вакансий:\n"
                              "1 - HeadHunter\n"
                              "2 - SuperJob\n"
                              "3 - совместный поиск\n"))

    search_text = input('Введите поисковый запрос (например, "python")\n')

    if choice_portal == 1:
        # инициализируем поиск вакансий на HeadHunter по поисковому запросу
        hh_list = get_hh_vacancies(search_text)
        print(f"Получено {len(hh_list)} вакансий\n"
              f"-------------------------------------")
        return hh_list

    if choice_portal == 2:
        # инициализируем поиск вакансий на SuperJob по поисковому запросу
        sj_list = get_sj_vacancies(search_text)
        print(f"Получено {len(sj_list)} вакансий\n"
              f"-------------------------------------")
        return sj_list

    if choice_portal == 3:
        # инициализируем поиск вакансий на Head Hunter и SuperJob по поисковому запросу
        hh_list = get_hh_vacancies(search_text)
        sj_list = get_sj_vacancies(search_text)

        # получаем общий список
        hh_sj_list = get_mixed_vacancies(hh_list, sj_list)
        print(f"Получено {len(hh_sj_list)} вакансий\n"
              f"-------------------------------------")
        return hh_sj_list


def get_hh_vacancies(search_text):
    """
    Получает список вакансий с HeadHunter
    :return:
    """
    get_hh_list = HeadHunterApi(search_text)  # инициализируем экземпляр класса

    get_hh_list.get_vacancies()  # получаем список вакансий с сайта в формате json

    hh_list_out = get_hh_list.vacancies_list  # получаем преобразованный список

    return hh_list_out


def get_sj_vacancies(search_text):
    """
    Получает список вакансий с SuperJob
    :return:
    """
    get_sj_list = SuperJobAPI(search_text)  # инициализируем экземпляр класса

    get_sj_list.get_vacancies()  # получаем список вакансий с сайта в формате json

    sj_list_out = get_sj_list.vacancies_list  # получаем преобразованный список

    return sj_list_out


def get_mixed_vacancies(list_1, list_2):
    """
    Собирает общий список вакансий,
    если пользователь выбирает совместный поиск по двум сайтам
    :param list_1:
    :param list_2:
    :return:
    """
    for item in list_2:
        list_1.append(item)

    return list_1


def end_program():
    print("Программа завершила работу")
    general_function(False)


def reading_json_file(file_data):
    """
    Считывает данные из файла в формате json
    :return:
    """
    with open(file_data, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    return data_list


if __name__ == '__main__':
    print("Программа предоставляет возможность поиска вакансий "
          "на порталах HeadHunter и SuperJob")
    general_function(True)
