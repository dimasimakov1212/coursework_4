from src.hh_service import HeadHunterApi
from src.sj_service import SuperJobAPI


def general_function():
    """
    Запускает основное тело программы
    :return:
    """

    print("Программа предоставляет возможностьпоиска вакансий"
          "на порталах Head Hunter и Super Job")

    choice_portal = int(input("Выберите место поиска вакансий:\n"
                              "1 - Head Hunter\n"
                              "2 - Super Job\n"
                              "3 - совместный поиск\n"))

    search_text = input('Введите поисковый запрос (например, "python"\n')

    if choice_portal == 1:
        # инициализируем поиск вакансий на Head Hunter по поисковому запросу
        hh_list = get_hh_vacancies(search_text)
        return print(hh_list)

    if choice_portal == 2:
        # инициализируем поиск вакансий на Super Job по поисковому запросу
        sj_list = get_sj_vacancies(search_text)
        return print(sj_list)


def get_hh_vacancies(search_text):
    """
    Получает список вакансий с Head Hunter
    :return:
    """
    get_hh_list = HeadHunterApi(search_text)

    get_hh_list.get_vacancies()  # получаем список вакансий с сайта в формате json

    hh_list_out = get_hh_list.vacancies_list  # получаем преобразованный список

    return hh_list_out


def get_sj_vacancies(search_text):
    """
    Получает список вакансий с SuperJob
    :return:
    """
    get_sj_list = SuperJobAPI(search_text)

    get_sj_list.get_vacancies()  # получаем список вакансий с сайта в формате json

    sj_list_out = get_sj_list.vacancies_list  # получаем преобразованный список

    return sj_list_out


if __name__ == '__main__':
    general_function()
