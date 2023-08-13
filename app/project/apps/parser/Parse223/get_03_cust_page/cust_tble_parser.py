class CustTable223Parser():
    """Класс получения и обработки главной страницы закупки"""
    def __init__(self, url, mode, get_class):
        """Храним сессию и устанавливаем заголовки"""
        self.urls = url
        self.referer = get_class.get_from_list(self, url, 'organization')
        self.page_content = ''
        self.params = None
        self.mode = mode
        self.page = ''
        self.get = get_class(self.referer, self.params, url, self.mode)

    def get_page(self):
        """Получаем страницу по запросу"""
        result = self.get.get()
        self.page = result
        return result

    def get_table_content(self):
        """Получаем содержимое таблицы"""
        res_dict = {}
        page_content = self.get_page()
        result = self.get.get_from_table(page_content)
        for i, dictionary in enumerate(result, start=1):
            if dictionary:
                key = f"cust_{i - 1}"
                res_dict[key] = dictionary
        return res_dict
