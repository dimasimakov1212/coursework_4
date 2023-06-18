from src.hh_service import HeadHunterApi
from src.sj_service import SuperJobAPI


def general_function():
    """
    Запускает основное тело программы
    :return:
    """

    print("Программа предоставляет возможностьпоиска вакансий"
          "на порталах HeadHunter и SuperJob")

    choice_portal = int(input("Выберите место поиска вакансий:\n"
                              "1 - HeadHunter\n"
                              "2 - SuperJob\n"
                              "3 - совместный поиск\n"))

    search_text = input('Введите поисковый запрос (например, "python")\n')

    if choice_portal == 1:
        # инициализируем поиск вакансий на HeadHunter по поисковому запросу
        hh_list = get_hh_vacancies(search_text)
        print(f"Получено {len(hh_list)} вакансий")

    if choice_portal == 2:
        # инициализируем поиск вакансий на SuperJob по поисковому запросу
        sj_list = get_sj_vacancies(search_text)
        print(f"Получено {len(sj_list)} вакансий")

    if choice_portal == 3:
        # инициализируем поиск вакансий на Head Hunter и SuperJob по поисковому запросу
        hh_list = get_hh_vacancies(search_text)
        sj_list = get_sj_vacancies(search_text)

        # получаем общий список
        hh_sj_list = get_mixed_vacancies(hh_list, sj_list)
        print(f"Получено {len(hh_sj_list)} вакансий")


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


if __name__ == '__main__':
    general_function()
