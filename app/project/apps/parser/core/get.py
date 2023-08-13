from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import re


def ua_generator():
    """Функция генерации user-agent"""
    ua = UserAgent(browsers=["chrome", "edge", "internet explorer", "firefox", "safari", "opera"])
    return ua.random


user_agent = ua_generator()


class Get():
    """Класс всех запросов"""
    def __init__(self, referer, params, url, mode):
        self.aclang = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        self.accept = 'text/html,application/xhtml+xml,' \
                      'application/xml;q=0.9,image/avif,' \
                      'image/webp,image/apng,*/*;q=0.8,' \
                      'application/signed-exchange;v=b3;q=0.7'
        self.session = requests.Session()
        self.user_agent = user_agent
        self.params = params
        self.ref = referer
        self.mode = mode
        self.url = url
        self.head = ''
        self.session.headers = {
            'Accept': self.accept,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': self.aclang,
            'Connection': 'keep-alive',
            'Host': 'zakupki.gov.ru',
            'Referer': self.ref,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent
        }

    def get_with_params(self):
        """Выполняем запрос с параметрами"""
        if self.mode == 'debug':
            print(' ')
            print(f"Выполнен запрос к странице  | '{self.url}'")
            print(f"Со страницы                 | '{self.ref}'")
            print(self.user_agent)
        response = self.session.get(self.url, params=self.params)
        status_code = response.status_code
        self.head = response.headers
        if status_code == 200:
            result = response.text
            if result:
                return result
            else:
                return None
        return None

    def get_without_params(self):
        """Выполняем запрос без параметров"""
        if self.mode == 'debug':
            print(' ')
            print(f"Выполнен запрос к странице  | '{self.url}'")
            print(f"Со страницы                 | '{self.ref}'")
            print(self.user_agent)
        response = self.session.get(self.url)
        status_code = response.status_code
        self.head = response.headers
        if status_code == 200:
            result = response.text
            if result:
                return result
            else:
                return None
        return None

    def request(self):
        """Выбираем тип запроса"""
        if self.params:
            return self.get_with_params()
        else:
            return self.get_without_params()

    def prettify(self, html_content):
        """Функция приведения html к человекочитаемости"""
        soup = BeautifulSoup(html_content, 'html.parser')
        prettified_html = soup.prettify()
        return prettified_html

    def get(self):
        """Возвращаем результат запроса"""
        request_result = self.request()
        result = self.prettify(request_result)
        return result

    def get_div(self, html_block, class_name):
        """Функция получения конкретного div из html"""
        soup = BeautifulSoup(html_block, 'html.parser')
        div_element = soup.find('div', class_=class_name)
        if div_element:
            return str(div_element)
        else:
            return None

    def get_div_by_id(self, html_block, class_id):
        """Функция получения конкретного div из html"""
        soup = BeautifulSoup(html_block, 'html.parser')
        div_element = soup.find('div', id=class_id)
        if div_element:
            return str(div_element)
        else:
            return None

    def get_divs(self, html_content, class_name):
        """Функция получения всех div из html по классу"""
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_=class_name)
        result = ''
        for div in divs:
            result += div.prettify()
        return result

    def get_spans(self, html_content, class_name):
        """Функция получения всех span из html по классу"""
        soup = BeautifulSoup(html_content, 'html.parser')
        spans = soup.find_all('span', class_=class_name)
        result = ''
        for span in spans:
            result += span.string or ''
        return result

    def get_script(self, html_content):
        """Функция получения кода первого непустого скрипта"""
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tags = soup.find_all('script', type="text/javascript")
        for script_tag in script_tags:
            script_content = script_tag.string
            if script_content and script_content.strip():
                return script_content.strip()
        return None

    def get_link(self, html_content):
        """Функция получения первой ссылки из html"""
        soup = BeautifulSoup(html_content, 'html.parser')
        link = soup.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            return href
        else:
            return None

    def get_links(self, html_content):
        """Функция получения всех ссылок из html"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def get_from_list(self, links, search_text):
        """Функция для поиска нужной ссылки"""
        for string in links:
            if search_text in string:
                return string
        return None

    def get_from_table(self, html):
        """Функция для парсинга HTML-таблицы"""
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        if not table:
            return None

        rows = []
        headers = []

        # Извлечение заголовков таблицы
        header_row = table.find('tr')
        if header_row:
            header_cells = header_row.find_all('th')
            headers = [cell.get_text(strip=True) for cell in header_cells]

        # Извлечение данных строк таблицы
        data_rows = table.find_all('tr')
        for row in data_rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            rows.append(row_data)

        # Создание списка словарей из заголовков и данных строк
        table_data = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                header = headers[i] if i < len(headers) else f"Column {i + 1}"
                row_dict[header] = value
            table_data.append(row_dict)

        return table_data

    def get_ajax_code(self, js_code):
        """Функция извлечения ajax из js"""
        ajax_code = ""
        ajax_pattern = r"\$.ajax\({(.*?)}\);"
        matches = re.findall(ajax_pattern, js_code, re.DOTALL)

        if matches:
            ajax_code = "\n".join(matches)

        return ajax_code

    def get_org_ajax(self, ajax_code):
        """Функция получения запроса организации из ajax"""
        url = ""
        data = {}

        # Извлечение URL
        url_match = re.search(r"url:\s*'([^']+)'", ajax_code)
        if url_match:
            url = url_match.group(1)

        # Извлечение данных
        data_match = re.search(r"data:\s*{([^}]+)}", ajax_code)
        if data_match:
            data_str = data_match.group(1)

            # Разбор данных в формате "ключ: значение"
            data_pairs = re.findall(r"(\w+):\s*'([^']+)'", data_str)
            data = {key: value for key, value in data_pairs}

        # Формирование полного URL-запроса
        full_url = f"https://zakupki.gov.ru{url}"
        if data:
            # Добавление параметров page и pageSize
            page = data.get("page", "1")
            pageSize = data.get("pageSize", "10")

            query_params = f"agencyId={data.get('agencyId')}&page={page}&pageSize={pageSize}"
            full_url = f"{full_url}?{query_params}"

        return full_url

    def get_config(self, file_path, section_name):
        """Метод парсинга конфигурационного файла"""
        section_lines = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            section_found = False

            for line in lines:
                line = line.strip()

                if line.startswith(';'):
                    continue  # Пропускаем строки с комментариями

                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    if current_section == section_name:
                        section_found = True
                    else:
                        section_found = False
                elif section_found:
                    section_lines.append(line)

        return section_lines

    def get_clean_list(self, list1, list2):
        """Удаление значений из list1, которые содержатся в list2"""
        return [x for x in list1 if x not in list2]

    def check_values_even_position(self, list1, list2):
        """Проверяет, находятся ли элементы из второго списка на чётных позициях в первом списке"""
        for value in list2:
            if value in list1:
                index = list1.index(value)
                if (index + 1) % 2 == 0:  # Изменение здесь
                    return False
        return True

    def get_list_even_length(self, list):
        """Проверка чётности длинны спаиска"""
        if len(list) % 2 == 0:
            return True
        else:
            return False

    def get_broken_field(self, list):
        """Ищем 'broken_field' в списке"""
        count = list.count('broken_field')
        if count >= 1:
            return True
        else:
            return False

    def set_broken_field(self, checked_dict, check_list, range_index):
        """Вставляем 'broken_field' если список изменён"""
        # print('Вызвана функция проверки')
        work_dict = checked_dict.copy()
        check_flag = False
        # print('Вызывана функция check')
        for i in range(range_index, len(work_dict)):
            if (i) % 2 != 0:
                if work_dict[i] in check_list:
                    # print('Найдено смещение')
                    index = i
                    check_flag = True
                    work_dict.insert(index, 'broken_field')
                    range_index += i + 1
                    break
        # print(check_flag)
        return [work_dict, check_flag, i]

    def get_list_check(self, checked_dict, check_list):
        """Меняем статус проверки списка с True на False если есть 'broken_field'"""
        work_dict = checked_dict
        check_flag = True
        check_counter = 0
        while check_flag:
            check_res = self.set_broken_field(work_dict, check_list, check_counter)
            work_dict = check_res[0]
            check_flag = check_res[1]
            check_counter = check_res[2]
        work_dict = work_dict[:-1]
        work_dict.append('False')
        return work_dict

    def convert_list_to_dict(self, list):
        """Преобразование списка в словарь"""
        dictionary = {}
        for i in range(0, len(list), 2):
            key = list[i]
            value = list[i + 1] if i + 1 < len(list) else None
            dictionary[key] = value
        return dictionary

    def get_parsed_titles(self, html, config_path, section_name):
        """Метод парсинга заголовков по словарю"""
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.find_all('div', class_=self.get_config(config_path, section_name))
        result_dict = []
        captions_text = [caption.text.strip() for caption in elements]
        for caption in captions_text:
            result_dict.append(caption)
        return result_dict

    def sort_titles(self, dict, add, exce):
        """Метод исключения ненужных заголовков"""
        dict.extend(add)
        result = [x for x in dict if x not in exce]
        return result
