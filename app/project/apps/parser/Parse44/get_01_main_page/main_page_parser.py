class MainPage44Parser():
    """Класс получения и обработки главной страницы закупки"""
    def __init__(self, lot_url, referer, mode, get_class):
        """Храним сессию и устанавливаем заголовки"""
        self.referer = referer
        self.url = lot_url
        self.params = None
        self.mode = mode
        self.page = ''
        self.get = get_class(self.referer, self.params, self.url, self.mode)

    def get_page(self):
        """Получаем страницу по запросу"""
        result = self.get.get()
        self.page = result
        return result

    def get_page_content(self):
        """Получаем содержимое страницы"""
        result = self.get.get_div(self.page, 'wrapper')
        return result

    def get_customer_link(self):
        """Получаем ссылку на заказчика"""
        result = self.get.get_divs(self.page, 'sectionMainInfo__body')
        link = self.get.get_link(result)
        return link

    def get_printform_links(self):
        """Получаем ссылку на печатную форму"""
        lst = []
        result = self.get.get_div(self.page, 'blockIcon')
        result = self.get.get_links(result)
        for link in result:
            lst.append('https://zakupki.gov.ru' + link)
        return lst

    def get_links_to_tabs(self):
        """Получаем все ссылки на вкладки"""
        result = self.get.get_div(self.page, 'tabsNav d-flex align-items-end')
        result = self.get.get_links(result)
        full_urls_list = []
        for link in result:
            url = 'https://zakupki.gov.ru' + link
            full_urls_list.append(url)
        customer_link = self.get_customer_link()
        full_urls_list.append(customer_link)
        printform_and_sign = self.get_printform_links()
        full_urls_list.extend(printform_and_sign)
        return full_urls_list
