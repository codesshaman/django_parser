from bs4 import BeautifulSoup


class LotData44Lexer():
    """Класс обработки лексем главной страницы закупки"""
    def __init__(self, content, func, get):
        """Получаем все необходимые функции"""
        self.get = get
        self.func = func
        self.content = content
        # # Словарь заголовков:
        # Добавляем сюда то, что нужно исключить из выборки
        self.titles = self.func.get_config('config44.ini', 'titles')
        # Словарь ключей:
        # Добавляем сюда только то, что должно быть ключами
        self.check = self.func.get_config('config44.ini', 'check')

    def get_every_customers_from_many(self):
        """Получаем словарь каждого заказчика из множества"""
        parsed = []
        soup = BeautifulSoup(self.content, 'html.parser')
        divs = soup.find_all('div', class_='blockInfo__collapse collapseInfo')
        for div in divs:

            parsed.append(div.get_text())

        return parsed

    def text_parse(self, content):
        """Метод парсинга текста"""

        # Создание объекта BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        self.func.remove_newlines_in_div(soup)
        self.func.clean_spaces(soup)
        # print(soup)

        # Получение чистых текстовых значений
        clear_text = soup.text
        text_lines = clear_text.split('\n')

        # Очищение текста от пустых строк
        lst = [line.strip() for line in text_lines if line.strip()]

        # Переименование дублируемых заголовков
        lst = self.func.rename_add_info(lst)

        # Удаление заголовков
        full_list = self.func.remove_titles(lst, self.titles)

        # Проверка на корректность заполнения
        check = self.func.check_values_even_position(full_list, self.check)

        # Проверка на чётную длинну
        even_len = self.func.get_list_even_length(full_list)
        if not even_len:
            # full_list.append('None')
            check = False

        # Добавление индикатора ошибки
        if check:
            full_list.append('mismatch')
            full_list.append('False')
        else:
            full_list.append('mismatch')
            full_list.append('True')

        if full_list[-1] == 'True':
            full_list = self.func.get_list_check(full_list, self.check)

        if self.func.get_broken_field(full_list):
            full_list.append('broken_fields')
            full_list.append('True')
        else:
            full_list.append('broken_fields')
            full_list.append('False')

        # Преобразование списка в словарь
        full_list = self.func.convert_list_to_dict(full_list)

        return full_list

    def get_cust_data(self):
        """Получаем словарь единственного заказчика"""
        customers = self.get_every_customers_from_many()
        custumer_lex = []
        if not customers:
            custumer_lex.append(self.text_parse(self.content))
        else:
            for customer in customers:
                custumer_lex.append(self.text_parse(customer))
        return custumer_lex
