def get_purchase_data(dictionary, key_nam):
    if key_nam in dictionary:
        return dictionary[key_nam]
    else:
        return None


def get_first_key(dictionary):
    if dictionary:
        first_key = next(iter(dictionary))
        return first_key
    else:
        return None


def extract_text_inside_quotes(text):
    start_index = text.find("«")
    end_index = text.find("»")
    if start_index != -1 and end_index != -1:
        extracted_text = text[start_index + 1:end_index]
        return extracted_text
    return None


def get_number(text):
    arr = text.split('=')
    return arr[1]


class Json44Answer():
    """Возвращаем json в нужном нам виде"""
    def __init__(self, dict, customers, links):
        self.dict = dict
        self.links = links
        self.success = True
        self.custs = customers
        self.numcusts = len(customers)
        self.fz_number = "44"
        self.contract_subject = None
        self.tender_link = self.links[0]
        self.purchase_number = get_number(self.tender_link)
        self.customer_email = None
        self.customer_phone = None
        self.customer_name = None
        self.customer_short_name = None
        self.customer_inn = None
        self.customer_kpp = None
        self.customer_ogrn = None
        self.customer_okpo = None
        self.customer_okato = None
        self.customer_reg_date = None
        self.customer_address = None
        self.customer_post_address = None
        self.lot_ikz = None
        self.lot_avance = None

    def purch_data(self, key):
        result = get_purchase_data(self.dict, key)
        if result:
            return result
        else:
            self.success = False

    def cust_data(self, dict, key):
        result = get_purchase_data(dict, key)
        if result:
            return result
        else:
            self.success = False

    def get_lot_data(self):
        lot_data = {}
        lot_data["num_lot_id"] = "1"
        lot_data["name"] = self.purch_data("Объект закупки")
        lot_data["max_price"] = self.purch_data("Начальная цена")
        lot_data["offered_price"] = self.purch_data("Начальная цена")
        lot_data["ikz"] = self.purch_data("Идентификационный код закупки (ИКЗ)")
        lot_data["avance"] = None
        return lot_data

    def get_customers(self):
        cust_data = []
        lot_data = self.get_lot_data()
        if self.numcusts > 1:
            for customer in self.custs:
                cust_ex = {}
                cust_ex["name"] = extract_text_inside_quotes(get_first_key(customer))
                cust_ex["lots"] = [lot_data]
                cust_data.append(cust_ex)
        else:
            cust_ex = {}
            cust_ex["name"] = self.purch_data("Организация, осуществляющая размещение")
            cust_ex["lots"] = [lot_data]
            cust_data.append(cust_ex)
        return cust_data

    def set_json_data(self):
        customer_data = self.get_customers()
        json_data = {}
        json_data["purchase_number"] = self.purchase_number
        json_data["fz_number"] = self.fz_number
        json_data["subject_contract"] = self.purch_data("Объект закупки")
        json_data["tender_link"] = self.tender_link
        json_data["email_customer"] = self.purch_data("Адрес электронной почты")
        json_data["phone_customer"] = self.purch_data("Телефон")
        json_data["reg_date"] = self.purch_data("Дата регистрации")
        json_data["address"] = self.purch_data("Место нахождения")
        json_data["customers"] = customer_data
        return json_data

    def purchase_info(self):
        purchase_info = {}
        json_data = self.set_json_data()
        purchase_info["success"] = self.success
        purchase_info["data"] = json_data
        return purchase_info


    # def get_customers(self):
    # def purch_data(self, key):
    #     result = get_purchase_data(self.dict, key)
    #     if result:
    #         return result
    #     else:
    #         self.success = False
    #
    # def lot_data(self, key):
    #     result = get_lot_data(self.dict, key)
    #     if result:
    #         return result
    #     else:
    #         self.success = False
    #
    # def set_purchase_number(self):
    #     result = self.purch_data("Реестровый номер извещения")
    #     self.purchase_number = result
    #     return result
    #
    # def set_contract_subject(self):
    #     result = self.purch_data("Наименование закупки")
    #     self.contract_subject = result
    #     return result
    #
    # def set_customer_email(self):
    #     result = self.purch_data("Адрес электронной почты")
    #     self.customer_email = result
    #     return result
    #
    # def set_customer_phone(self):
    #     result = self.purch_data("Контактный телефон")
    #     self.customer_phone = result
    #     return result
    #
    # def set_customer_name(self):
    #     result = self.purch_data("Полное наименование")
    #     self.customer_name = result
    #     return result
    #
    # def set_customer_short_name(self):
    #     result = self.purch_data("Сокращенное наименование")
    #     self.customer_short_name = result
    #     return result
    #
    # def set_customer_inn(self):
    #     result = self.purch_data("ИНН")
    #     self.customer_inn = result
    #     return result
    #
    # def set_customer_kpp(self):
    #     result = self.purch_data("КПП")
    #     self.customer_kpp = result
    #     return result
    #
    # def set_customer_ogrn(self):
    #     result = self.purch_data("ОГРН")
    #     self.customer_ogrn = result
    #     return result
    #
    # def set_customer_okpo(self):
    #     result = self.purch_data("Код по ОКПО")
    #     self.customer_okpo = result
    #     return result
    #
    # def set_customer_okato(self):
    #     result = self.purch_data("Код по ОКАТО")
    #     self.customer_okato = result
    #     return result
    #
    # def set_customer_reg_date(self):
    #     result = self.purch_data("Дата регистрации")
    #     self.customer_reg_date = result
    #     return result
    #
    # def set_customer_address(self):
    #     result = self.purch_data("Место нахождения")
    #     self.customer_address = result
    #     return result
    #
    # def set_customer_post_address(self):
    #     result = self.purch_data("Почтовый адрес")
    #     self.customer_post_address = result
    #     return result
    #
    # def get_lot_name(self):
    #     result = self.lot_data("Наименование предмета договора (лота)")
    #     self.lots_names.append(result)
    #     return result
    #
    # def get_lot_id(self):
    #     result = self.lot_data("Номер лота")
    #     self.lots_ids.append(result)
    #     return result
    #
    # def get_lot_max_price(self):
    #     result = self.lot_data("Начальная (максимальная) цена договора (цена лота)")
    #     self.lots_max_prices.append(result)
    #     return result
    #
    # def get_lot_offered_price(self):
    #     result = self.lot_data("Начальная (максимальная) цена договора (цена лота)")
    #     self.lots_offered_prices.append(result)
    #     return result
    #
    # def set_lots_list(self):
    #     self.get_lot_id()
    #     self.get_lot_name()
    #     self.get_lot_max_price()
    #     self.get_lot_offered_price()
    #     lots_list = []
    #     counter = 0
    #     for lot_id in self.lots_ids[0]:
    #         current_dict = {}
    #         current_dict.clear()
    #         current_dict["num_lot_id"] = lot_id
    #         current_dict["name"] = self.lots_names[0][counter]
    #         current_dict["max_price"] = self.lots_max_prices[0][counter]
    #         current_dict["offered_price"] = self.lots_offered_prices[0][counter]
    #         current_dict["ikz"] = self.lot_ikz
    #         current_dict["avance"] = self.lot_avance
    #         lots_list.append(current_dict)
    #         counter += 1
    #     return lots_list
    #
    # def set_customer_data(self):
    #     lots_list = self.set_lots_list()
    #     customer_data = {}
    #     customer_data["name"] = self.set_customer_name()
    #     customer_data["inn"] = self.set_customer_inn()
    #     customer_data["kpp"] = self.set_customer_kpp()
    #     customer_data["ogrn"] = self.set_customer_ogrn()
    #     customer_data["okpo"] = self.set_customer_okpo()
    #     customer_data["okato"] = self.set_customer_okato()
    #     customer_data["reg_date"] = self.set_customer_reg_date()
    #     customer_data["address"] = self.set_customer_address()
    #     customer_data["post_address"] = self.set_customer_post_address()
    #     customer_data["lots"] = lots_list
    #     return customer_data
    #
    # def set_json_data(self):
    #     customer_data = self.set_customer_data()
    #     json_data = {}
    #     json_data["purchase_number"] = self.set_purchase_number()
    #     json_data["fz_number"] = self.fz_number
    #     json_data["subject_contract"] = self.set_contract_subject()
    #     json_data["tender_link"] = self.tender_link
    #     json_data["email_customer"] = self.set_customer_email()
    #     json_data["phone_customer"] = self.set_customer_phone()
    #     json_data["reg_date"] = self.set_customer_reg_date()
    #     json_data["address"] = self.set_customer_address()
    #     json_data["customers"] = [customer_data]
    #     return json_data
    #
    # def purchase_info(self):
    #     purchase_info = {}
    #     json_data = self.set_json_data()
    #     purchase_info["success"] = self.success
    #     purchase_info["data"] = json_data
    #     return purchase_info
