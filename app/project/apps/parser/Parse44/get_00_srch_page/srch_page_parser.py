import bs4


def records_checker(html):
    """Проверяем существование записей"""
    soup = bs4.BeautifulSoup(html, 'html.parser')
    results = soup.find(class_='search-results__total').get_text(strip=True)
    array = results.split(' ')
    number = array[0]
    result = int(number)
    return result


class SrchPage44Parser():
    """Класс получения и обработки страницы поискового запроса"""

    def __init__(self, lot_id, mode, get_class):
        """Храним сессию и устанавливаем заголовки"""
        self.mode = mode
        self.id = lot_id
        self.params = {
            'morphology': 'on',
            'search-filter': 'Релевантности',
            'pageNumber': '1',
            'sortDirection': 'false',
            'recordsPerPage': '_10',
            'showLotsInfoHidden': 'false',
            'sortBy': 'RELEVANCE',
            'fz44': 'on',
            'currencyIdGeneral': '-1'
        }
        self.referer = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
        self.url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=" + self.id
        self.get = get_class(self.referer, self.params, self.url, self.mode)

    def get_search_link(self):
        """Получаем ссылку на закупку"""
        block = self.get.get_div(self.get.get(), 'registry-entry__header-mid__number')
        link = self.get.get_link(block)
        if link:
            link = 'https://zakupki.gov.ru' + link
            return [True, link, self.referer]
        return [False, None, None]
