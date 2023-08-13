from django.http import HttpResponse
from .parse223 import Parse223
from .parse44 import Parse44
import json
import re


def lower_keys(dictionary):
    translated_dict = {}
    for key, value in dictionary.items():
        translated_key = re.sub(r'[^\w\s]', '', key).lower().replace(' ', '_')
        translated_dict[translated_key] = value
    return translated_dict


def translate_dict(d):
    """
    Функция принимает словарь d и заменяет все кириллические символы ключей на латиницу.
    Она возвращает новый словарь с измененными ключами, значения остаются неизменными.
    """
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya'
    }
    new_d = {}
    for k, v in d.items():
        new_key = ''
        for c in k:
            if c.lower() in mapping:
                if c.isupper():
                    new_key += mapping[c.lower()].capitalize()
                else:
                    new_key += mapping[c]
            else:
                new_key += c
        new_d[new_key] = v
    return new_d


def dict_to_json(data):
    """
    Функция для преобразования словаря в json.
    :param data: словарь python
    :return: строка в формате json
    """
    return json.dumps(data)


# Create your views here.
def parser_view(request, lot_id):
    """Метод, запускающий парсер"""
    length = len(lot_id)
    if length < 13:
        parser = Parse223(lot_id)
    if length > 13:
        parser = Parse44(lot_id)
    result = parser.unificateur()
    # result = parser.parse_link()
    # result = lower_keys(result)
    # result = translate_dict(result)
    # result = dict_to_json(result)
    # response.headers['Content-Type'] = 'application/json; charset=utf-8'
    # json_data = json.dumps(result, ensure_ascii=False)
    json_data = json.dumps(result)
    headers = {'Content-Type': 'application/json'}
    response = HttpResponse(json_data, headers)
    # return HttpResponse(f'{result}')
    return response
