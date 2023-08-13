from bs4 import BeautifulSoup
from lxml import etree


class LotsPage223Parser():
    """Класс получения и обработки главной страницы закупки"""
    def __init__(self, urls_list, mode, get_class):
        """Храним сессию и устанавливаем заголовки"""
        self.urls = urls_list
        self.referer = self.urls[0]
        self.params = None
        self.mode = mode
        self.page = ''
        self.get = get_class(self.referer, self.params, get_class.get_from_list(self, urls_list, 'lot-list'), self.mode)

    def get_page(self):
        """Получаем страницу по запросу"""
        result = self.get.get()
        self.page = result
        return result

    def get_lots_content(self):
        """Получаем содержимое страницы"""
        result = self.get.get_div(self.page, 'card-common')
        return result

    # def get_lots_table(self):
    #     """Парсинг таблицы стандартным методом"""
    #     res_list = []
    #     result = self.get.get_div(self.page, 'card-common')
    #     result = self.get.get_from_table(result)
    #     for dict in result:
    #         if dict != {}:
    #             res_list.append(dict)
    #     return res_list

    def get_lots_table(self):
        html = self.get.get_div(self.page, 'card-common')
        # Создаем объект ElementTree из HTML-строки
        tree = etree.HTML(html)

        # Находим все строки таблицы
        rows = tree.xpath("//table//tr")

        # Получаем заголовки столбцов из первой строки таблицы
        headers = [header.text.strip() for header in rows[0].xpath("th|td")]

        # Создаем пустой словарь для хранения данных
        data_dict = {}

        # Обрабатываем каждую строку таблицы, начиная со второй строки
        for i, row in enumerate(rows[1:], start=1):
            # Получаем значения ячеек строки и обрабатываем их
            values = [cell.text for cell in row.xpath("td")]
            values = [value.strip().replace('\xa0', ' ').replace('\n', ' ') for value in values]
            values = [' '.join(value.split()) for value in values]

            # Проверяем, что строка не содержит только пустые значения
            if any(values):
                # Создаем словарь для текущей строки, используя заголовки столбцов в качестве ключей
                row_dict = {header: value for header, value in zip(headers, values)}

                # Проверяем, что словарь не пустой
                if any(row_dict.values()):
                    # Создаем ключ в формате "lot_i" и добавляем словарь текущей строки в общий словарь данных
                    lot_key = f"lot_{i}"
                    data_dict[lot_key] = row_dict

        return data_dict

    def get_lots_links(self):
        soup = BeautifulSoup(self.get_page(), 'html.parser')
        links = []
        table_rows = soup.find_all('tr')

        for row in table_rows:
            link = row.find('a')
            if link:
                href = link.get('href')
                links.append('https://zakupki.gov.ru/' + href)

        return links

    def merge_dicts(self):
        """Объединение результата парсинга в один словарь"""
        dicts = self.get_lots_table()
        merged_dict = {}
        for key, dictionary in dicts.items():
            if dictionary:  # Проверяем, что словарь не пустой
                merged_dict.update(dictionary)
        return merged_dict
