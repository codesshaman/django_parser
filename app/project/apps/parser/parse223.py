import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
# core_dir = os.path.join(current_dir)
# print(core_dir)
sys.path.append(current_dir)
from core import func
from core.get import Get
from Parse223.set_json.json223 import Json223Answer
from Parse223.get_00_srch_page.srch_page_parser import SrchPage223Parser
from Parse223.get_01_main_page.main_page_parser import MainPage223Parser
from Parse223.get_01_main_page.main_page_lexer import MainPage223Lexer
from Parse223.get_02_lots_page.lots_page_parser import LotsPage223Parser
from Parse223.get_02_lots_page.lot_page_parser import LotPage223Parser
from Parse223.get_02_lots_page.lot_page_lexer import LotPage223Lexer
from Parse223.get_03_cust_page.cust_page_parser import CustPage223Parser
from Parse223.get_03_cust_page.cust_tble_parser import CustTable223Parser
from Parse223.get_03_cust_page.cust_page_lexer import CustPage223Lexer


class Parse223():
    """Основной класс парсера"""
    def __init__(self, lot_id):
        self.main_page_content = ''
        self.main_page_dictjson = {}
        self.lots_page_content = ''
        self.lots_page_table = {}
        self.cust_page_content = ''
        self.cust_page_dictjson = {}
        self.cust_page_table = {}
        self.cust_page_link = None
        self.all_pages_links = []
        self.referer = ''
        self.id = lot_id
        self.mode = 'debug'

    def parse_link(self):
        """Метод получения ссылки на закупку"""
        # Получаем объект парсера
        parser = SrchPage223Parser(self.id, self.mode, Get)
        # Инициализируем объект парсера и получаем ссылку
        result = parser.get_search_link()
        # Проверяем и возвращаем ссылку
        if result[0]:
            self.referer = result[2]
            return result[1]
        raise FileNotFoundError(f"Что-то пошло не так на этапе парсинга ссылки на закупку")

    def parse_main_page(self):
        """********************************************************************************
        *********************Метод получения данных с главной страницы*******************
        ********************************************************************************"""
        # Выполняем предыдущую функцию
        link = self.parse_link()
        # Получаем объект парсера
        main_parser = MainPage223Parser(link, self.referer, self.mode, Get)
        # Инициализируем парсер
        main_parser.get_page()
        # Получаем содержимое страницы
        result = main_parser.get_page_content()
        # Сохраняем содержимое страницы
        self.main_page_content = main_parser.get.prettify(result)
        # Получаем все вкладки
        result = main_parser.get_links_to_tabs()
        # Сохраняем полученные ссылки
        self.all_pages_links = result
        # Сохраняем страницу перехода
        if result:
            self.referer = self.all_pages_links[0]
        # Возвращаем результат
        return result

    def main_page_lexer(self):
        """Лексер главной страницы"""
        # Инициализируем предыдущий уровень
        self.parse_main_page()
        # Получаем содержимое страницы
        content = self.main_page_content
        # Получаем объект лексера
        main_lexer = MainPage223Lexer(content, func)
        # Получаем конечный словарь
        result = main_lexer.text_parse()
        # Сохраняем конечный словарь
        self.main_page_dictjson = result
        return result

    def parse_lot_page(self):
        """********************************************************************************
        *********************Метод получения данных со страницы лотов********************
        ********************************************************************************"""
        # Инициализируем предыдущий уровень
        self.main_page_lexer()
        # Получаем список ссылок
        links = self.all_pages_links
        # Получаем объект парсера
        lots_parser = LotsPage223Parser(links, self.mode, Get)
        # Инициализируем парсер
        lots_parser.get_page()
        # Получаем содержимое страницы лотов
        result = lots_parser.get_lots_content()
        # Сохраняем содержимое страницы лотов
        self.lots_page_content = result
        # Получаем таблицу лотов
        result = lots_parser.get_lots_table()
        # Получаем ссылки на каждый лот:
        lots_links = lots_parser.get_lots_links()
        # добавляем полученные ссылки в список ссылок
        # self.all_pages_links.append(links)
        # Вытаскиваем информацию по всем лотам
        lots_list = {}
        counter = 1
        for link in lots_links:
            if self.mode == 'debug':
                print(lots_links[counter - 1])
            lot_name = 'lot_' + str(counter)
            lot_parser = LotPage223Parser(link, self.all_pages_links[-1], self.mode, Get)
            answer = lot_parser.get_page_content()
            # Получаем объект лексера
            lexer = LotPage223Lexer(answer, func)
            answer = lexer.text_parse()
            lots_list[lot_name] = answer
            self.all_pages_links.append(link)
            counter += 1
        result = lots_list
        # Сохраняем таблицу лотов
        self.lots_page_table = result
        # Возвращаем результат
        return result

    # def lot_page_lexer(self):
    #     """Лексер страницы лотов"""
    #     # Инициализируем предыдущий уровень
    #     self.parse_lot_page()
    #     # Получаем объект лексера
    #     lots_lexer = LotsPage223Lexer(self.lots_page_table, func, Get)
    #     # Получаем словарь
    #     dictlist = self.main_page_dictjson
    #     # Обрабатываем словарь
    #     result = lots_lexer.dict_list_cleaner()
    #     # Сохраняем таблицу лотов
    #     self.lots_page_table = result
    #     return result

    def parse_customer_page(self):
        """********************************************************************************
        *******************Метод получения данных со страницы заказчика******************
        ********************************************************************************"""
        # Инициализируем предыдущий уровень
        self.parse_lot_page()
        # Получаем список ссылок
        links = self.all_pages_links
        # Получаем объект парсера
        cus_parser = CustPage223Parser(links, self.mode, Get)
        # Инициализируем парсера
        cus_parser.get_page()
        # Получаем ссылку на таблицу закупки
        result = cus_parser.get_table_link()
        # Проверяем, есть ли таблица на странице:
        if result:
            self.cust_page_link = result
        # Получаем содержимое страницы заказчика
        result = cus_parser.get_page_content()
        # Сохраняем содержимое страницы заказчика
        self.cust_page_content = result
        return result

    def custumer_page_lexer(self):
        # Инициализируем предыдущий уровень
        self.parse_customer_page()
        # Получаем объект лексера
        cus_parser = CustPage223Lexer(self.cust_page_content, func, Get)
        # Инициализируем лексер
        result = cus_parser.text_parse()
        # Записываем результат
        self.cust_page_dictjson = result
        return result

    def parse_customer_table(self):
        """********************************************************************************
        ********************Метод получения данных из таблицы заказчиков******************
        ********************************************************************************"""
        # Инициализируем предыдущий уровень:
        self.custumer_page_lexer()
        # Получаем ссылку на страницу
        link = self.cust_page_link
        if link:
            # Получаем объект парсера
            cus_parser = CustTable223Parser(link, self.mode, Get)
            # Получаем ссылку на таблицу
            result = cus_parser.get_table_content()
            # Сохраняем содержимое таблицы
            self.cust_page_table = result
            return result
        else:
            return None

    def unificateur(self):
        # Инициализируем предыдущий уровень
        self.parse_customer_table()
        # Объединяем словари
        result = func.merge_dicts(
            self.main_page_dictjson,
            self.lots_page_table,
            self.cust_page_table,
            self.cust_page_dictjson
        )
        set_json_obj = Json223Answer(result, self.all_pages_links)
        result = set_json_obj.purchase_info()
        return result


purchase_id = '32312555094'
# # purchase_id = '32312567652'
# mode = 'debug'
#
#
# def get_search_page_test():
#     """Функция для тестов запросов к странице поиска"""
#     referer = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
#     params = {
#                 'morphology': 'on',
#                 'search-filter': 'Релевантности',
#                 'pageNumber': '1',
#                 'sortDirection': 'false',
#                 'recordsPerPage': '_10',
#                 'showLotsInfoHidden': 'false',
#                 'sortBy': 'RELEVANCE',
#                 'fz223': 'on',
#                 'currencyIdGeneral': '-1'
#             }
#     url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=" + purchase_id
#     requester = Get(referer, params, url, mode)
#     result = requester.get()
#     return result
#
# # Все методы объекта парсера:
# # parse_main_page
# # main_page_lexer
# # parse_lot_page
# # lot_page_lexer
# # parse_customer_page
# # custumer_page_lexer
# # parse_customer_table


def main():
    parser = Parse223(purchase_id)
    content = parser.unificateur()

    print(content)
    # print(get_search_page_test())


if __name__ == '__main__':
    main()
