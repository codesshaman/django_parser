from bs4 import BeautifulSoup

class LotData44Parser():
    """Класс получения и обработки главной страницы закупки"""
    def __init__(self, content, get):
        """Храним сессию и устанавливаем заголовки"""
        self.content = content
        self.cust = None
        self.get = get
        self.page = ''

    def get_customer_section(self):
        """Получаем секцию с заказчиками"""
        result = self.get.get_div_by_id(self, self.content, 'custReqNoticeTable')
        self.cust = result
        # print(result)
        return result
