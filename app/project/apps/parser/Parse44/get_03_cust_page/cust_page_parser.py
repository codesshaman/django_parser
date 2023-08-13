class CustPage44Parser():
    """Класс получения и обработки главной страницы закупки"""
    def __init__(self, urls_list, mode, get_class):
        """Храним сессию и устанавливаем заголовки"""
        self.urls = urls_list
        self.referer = self.urls[0]
        self.page_content = ''
        self.params = None
        self.mode = mode
        self.page = ''
        self.get = get_class(self.referer, self.params, get_class.get_from_list(self, urls_list, 'organization'), self.mode)

    def get_page(self):
        """Получаем страницу по запросу"""
        result = self.get.get()
        self.page = result
        return result

    def get_page_content(self):
        """Получаем содержимое страницы"""
        result = self.get.get_div(self.page, 'tabs-container')
        self.page_content = result
        return result

    def get_table_link(self):
        """Получаем содержимое таблицы"""
        self.get_page_content()
        result = self.get.get_divs(self.page, 'tabs-container')
        result = self.get.get_script(result)
        if not result:
            result = None
        else:
            result = self.get.get_ajax_code(result)
            result = self.get.get_org_ajax(result)
        return result

    def get_table_data(self):
        link = self.get_table_link()
        if link:
            return link