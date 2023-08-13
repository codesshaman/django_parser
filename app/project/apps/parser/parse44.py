import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from core import func
from core.get import Get
from Parse44.set_json.json44 import Json44Answer
from Parse44.get_00_srch_page.srch_page_parser import SrchPage44Parser
from Parse44.get_01_main_page.main_page_parser import MainPage44Parser
from Parse44.get_01_main_page.main_page_lexer import MainPage44Lexer
from Parse44.get_02_lots_data.lot_data_parser import LotData44Parser
from Parse44.get_02_lots_data.lot_data_lexer import LotData44Lexer
from Parse44.get_03_cust_page.cust_page_parser import CustPage44Parser
from Parse44.get_03_cust_page.cust_tble_parser import CustTable44Parser
from Parse44.get_03_cust_page.cust_page_lexer import CustPage44Lexer


class Parse44():
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
        self.custumers_data = None
        self.all_pages_links = []
        self.all_custumers = None
        self.referer = ''
        self.id = lot_id
        self.mode = 'free'

    def parse_link(self):
        """Метод получения ссылки на закупку"""
        # Получаем объект парсера
        parser = SrchPage44Parser(self.id, self.mode, Get)
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
        main_parser = MainPage44Parser(link, self.referer, self.mode, Get)
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
        main_lexer = MainPage44Lexer(content, func, Get)
        # Получаем конечный словарь
        result = main_lexer.text_parse()
        # Сохраняем конечный словарь
        self.main_page_dictjson = result
        return result

    def parse_custs_data(self):
        """********************************************************************************
        ************************Метод получения данных о заказчиках**********************
        ********************************************************************************"""
        # Инициализируем предыдущий уровень
        self.main_page_lexer()
        # Получаем объект парсера
        cus_parser = LotData44Parser(self.main_page_content, Get)
        # Парсим всех заказчиков
        result = cus_parser.get_customer_section()
        # Заносим заказчиков в класс
        self.all_custumers = result
        return result

    def custs_data_lexer(self):
        # Инициализируем предыдущий уровень
        self.parse_custs_data()
        # Получаем объект лексера
        custs_lexer = LotData44Lexer(self.all_custumers, func, Get)
        # Инициализируем лексер
        result = custs_lexer.get_cust_data()
        # Записываем результат
        self.custumers_data = result
        return result

    def parse_customer_page(self):
        """********************************************************************************
        *******************Метод получения данных со страницы заказчика******************
        ********************************************************************************"""
        # Инициализируем предыдущий уровень
        self.custs_data_lexer()
        # Получаем список ссылок
        links = self.all_pages_links
        # Получаем объект парсера
        cus_parser = CustPage44Parser(links, self.mode, Get)
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
        cus_parser = CustPage44Lexer(self.cust_page_content, func, Get)
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
            cus_parser = CustTable44Parser(link, self.mode, Get)
            # Получаем ссылку на таблицу
            result = cus_parser.get_table_content()
            # Сохраняем содержимое таблицы
            self.cust_page_table = result
            return result
        else:
            return None

    def unificateur(self):
        # Инициализируем предыдущий уровень
        self.custumer_page_lexer()
        # Объединяем словари
        dict = func.merge_dicts(
            self.main_page_dictjson,
            self.lots_page_table,
            self.cust_page_table,
            self.cust_page_dictjson
        )
        set_json_obj = Json44Answer(dict, self.custumers_data, self.all_pages_links)
        result = set_json_obj.purchase_info()
        return result


purchase_id = '0319200064423000083'


def main():
    parser = Parse44(purchase_id)
    content = parser.unificateur()
    print(content)
    # print(get_search_page_test())


if __name__ == '__main__':
    main()
