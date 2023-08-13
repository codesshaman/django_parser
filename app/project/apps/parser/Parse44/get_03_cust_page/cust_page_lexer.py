from bs4 import BeautifulSoup


class CustPage44Lexer():
    """Класс обработки лексем главной страницы закупки"""
    def __init__(self, content, func, get):
        """Получаем все необходимые функции"""
        self.get = get
        self.func = func
        self.content = content
        # Словарь заголовков
        self.dict = self.func.get_config('config223.ini', 'titles_class')
        # Словарь дополнительных заголовков:
        # Добавляем сюда то, что нужно исключить из выборки
        self.add = self.func.get_config('config223.ini', 'cust_titles')
        # Словарь заголовков-исключений:
        # Добавляем сюда те заголовки, которые будут отображаться
        self.exce = self.func.get_config('config223.ini', 'cust_passing')
        # Словарь проверочных заголовков:
        # Добавляем сюда только то, что должно быть ключами
        self.check = self.func.get_config('config223.ini', 'cust_check')
        # Словарь пропускаемыхных заголовков:
        # Добавляем сюда заголовки, содержимое которых нужно пропустить
        self.skip = self.func.get_config('config223.ini', 'cust_skip')

    def text_parse(self):
        """Метод парсинга текста"""

        # Создание объекта BeautifulSoup
        soup = BeautifulSoup(self.content, 'html.parser')
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

        # Пропуск ненужных значений
        lst = self.func.filter_values(lst, self.check, self.skip)

        # Удаление заголовков
        full_list = self.func.remove_titles(lst, self.add)
        # full_list = self.func.get_clean_list(lst, exc)

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

        # if self.func.get_broken_field(full_list):
        #     full_list.append('broken_fields')
        #     full_list.append('True')
        # else:
        #     full_list.append('broken_fields')
        #     full_list.append('False')

        # Преобразование списка в словарь
        full_list = self.func.convert_list_to_dict(full_list)

        return full_list
