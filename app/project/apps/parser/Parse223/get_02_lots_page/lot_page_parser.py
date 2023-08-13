class LotPage223Parser():
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
        self.get_page()
        result = self.get.get_div(self.page, 'card-common')
        return result
