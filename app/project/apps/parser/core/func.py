import json


def convert_dict_to_json(dictionary):
    """Переводим словарь в json"""
    json_data = json.dumps(dictionary)
    return json_data


def rename_add_info(data_list):
    """Переименование повторяющихся значений"""
    renamed_list = []
    prev_value = None

    for value in data_list:
        if value == "Дополнительная информация" and prev_value == "Дополнительная информация":
            renamed_list.append("Дополнительные данные")
        else:
            renamed_list.append(value)
        prev_value = value

    for value in data_list:
        if value == "Начальная (максимальная) цена контракта" and prev_value == "Начальная (максимальная) цена контракта":
            renamed_list.append("Начальная максимальная цена контракта")
        else:
            renamed_list.append(value)
        prev_value = value

    for value in data_list:
        if value == "Сведения о связи с позицией плана-графика" and prev_value == "Сведения о связи с позицией плана-графика":
            renamed_list.append("Связь с позицией плана-графика")
        else:
            renamed_list.append(value)
        prev_value = value



    return renamed_list


def get_config(file_path, section_name):
    """Функция парсинга конфигурационного файла"""
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


def remove_titles(list1, list2):
    """Функция исключения заголовков"""
    result = []
    for value in list1:
        if value not in list2:
            result.append(value)
    return result


def clean_spaces(soup):
    """Очищаем текст от лишних пробелов"""
    for tag in soup.find_all():
        if tag.string:
            tag.string = ' '.join(tag.get_text().split())


def get_clean_list(list1, list2):
    """Удаление значений из list1, которые содержатся в list2"""
    return [x for x in list1 if x not in list2]


def remove_newlines_in_div(soup):
    """Удаляем переносы внутри блоков"""
    for tag in soup.find_all():
        if tag.string:
            tag.string = tag.get_text().replace('\n', '')


def check_values_even_position(list1, list2):
    """Проверяет, находятся ли элементы из второго списка на чётных позициях в первом списке"""
    for value in list2:
        if value in list1:
            index = list1.index(value)
            if (index + 1) % 2 == 0:  # Изменение здесь
                return False
    return True


def get_list_even_length(list):
    """Проверка чётности длинны спаиска"""
    if len(list) % 2 == 0:
        return True
    else:
        return False


def set_broken_field(checked_dict, check_list, range_index):
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


def get_list_check(checked_dict, check_list):
    """Меняем статус проверки списка с True на False если есть 'broken_field'"""
    work_dict = checked_dict
    check_flag = True
    check_counter = 0
    while check_flag:
        check_res = set_broken_field(work_dict, check_list, check_counter)
        work_dict = check_res[0]
        check_flag = check_res[1]
        check_counter = check_res[2]
    work_dict = work_dict[:-1]
    work_dict.append('False')
    return work_dict


def convert_list_to_dict(list):
    """Преобразование списка в словарь"""
    dictionary = {}
    for i in range(0, len(list), 2):
        key = list[i]
        value = list[i + 1] if i + 1 < len(list) else None
        dictionary[key] = value
    return dictionary


def get_broken_field(list):
    """Ищем 'broken_field' в списке"""
    count = list.count('broken_field')
    if count >= 1:
        return True
    else:
        return False


def remove_duplicate_phrases(input_string):
    """Удаление повторяющихся фраз"""
    phrase = ""
    result = ""
    for char in input_string:
        phrase += char
        if input_string.count(phrase) * len(phrase) == len(input_string):
            result = phrase
            break
    if result == "":
        return input_string
    else:
        return result


def clean_dictionary_list(dictionary):
    """Очищаем список от лишних символов"""
    cleaned_dictionary = {}
    for key, value in dictionary.items():
        cleaned_value = value.replace('\n', ' ')  # Заменяем символы переноса на пробелы
        cleaned_value = ' '.join(cleaned_value.split())  # Удаляем лишние пробелы
        cleaned_value = cleaned_value.replace('\xa0', ' ')  # Заменяем символ \xa0 на пробел
        cleaned_value = remove_duplicate_phrases(cleaned_value)
        cleaned_dictionary[key] = cleaned_value
    return cleaned_dictionary


def filter_values(all_values, headers, skip_headers):
    filtered_values = []
    skip = False

    for value in all_values:
        if value in skip_headers:
            skip = True
        elif value in headers:
            skip = False
            filtered_values.append(value)

        if not skip:
            filtered_values.append(value)

    return filtered_values


def merge_dicts(*dicts):
    """Функция объединения словарей"""
    merged_dict = {}
    for arg in dicts:
        if isinstance(arg, dict):
            merged_dict.update(arg)
    return merged_dict
