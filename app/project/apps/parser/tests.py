from parse223 import Parse223


purchase_id = '32312554306'
mode = 'debug'


def check_broken_field(dictionary):
    for value in dictionary.values():
        if isinstance(value, dict):
            if "broken_field" in value:
                return True
    return False


def main():
    for id in range(32312249098, 32312554306):
        purchase_id = str(id)
        parser = Parse223(purchase_id, mode)
        print(type(parser))
        content = parser.custumer_page_lexer()
        check = check_broken_field(content)
        print(content)
        if check:
            print('ЕСТЬ БИТОЕ ПОЛЕ!!!')
        input("Нажмите Enter, чтобы продолжить...")
    # print(get_search_page_test())


if __name__ == '__main__':
    main()
