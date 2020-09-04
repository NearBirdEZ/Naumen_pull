import time
from selenium.common.exceptions import NoSuchElementException
import create_list_kkt

bad_not_service = {}  # У магазинов отсутвует услуга
register_requests = {}  # зарегистрированные заявки магазин :  номер
driver = create_list_kkt.driver


def find_shop(shop: str):
    """Функция поиска по магазину"""
    index_url = "http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid=corebofs000080000ikhm8pnur5l85oc"
    driver.get(index_url)
    create_list_kkt.enter_words("searchString", shop)
    driver.find_element_by_id("doSearch").click()


def create_request(serial_number: str,
                   contact_human: str,
                   contact_phone: str,
                   contact_email: str):
    time.sleep(1)
    """Заполнение выпадающих списков 
    - Привязать к Плановая замена ФН
    - Тип запроса New
    - Канал приема заявки Email"""

    lst_xpath = ['//*[@id="link_object"]/option[@nonshifted="ККТ: Плановая замена ФН"]',
                 '// *[ @ id = "servicecall_case"] / option[@nonshifted="new"]',
                 '//*[@id="valuefabaseo2k2u0o0000lch8jk1k366sge8"]/option[@nonshifted="По электронной почте"]']
    for xpath in lst_xpath:
        driver.find_element_by_xpath(xpath).click()
        time.sleep(0.5)

    """Заполнение полей словами"""
    serial_numbers = ["ККТ № " + line.split("_")[0] + " Срок действия " + line.split("_")[1]
                      for line in serial_number.split()]

    serial_numbers = "\n".join(serial_numbers)

    text_area = f"Требуется замена ФН\n{serial_numbers}"

    dict_id_area = {"call_description": text_area,
                    "contact_human": contact_human,
                    "contact_phone": contact_phone,
                    "contact_email": contact_email}

    for id_object in dict_id_area:
        create_list_kkt.enter_words(id_object, dict_id_area[id_object])
    driver.find_element_by_id("add").click()


def add_kkt_and_register(serial_numbers, shop):
    """Функция для добавления ресурсов к заявке и перевод в статус "зарегистрирована"""

    "Сохраняем сылку на зарегистрированную заявку и ее номер"
    link_request = driver.find_element_by_xpath('//*[@id="navpath"]/a[3]').get_attribute("href").split("?")[-1]
    link_take = driver.find_element_by_xpath('//*[@id="ServiceCall.ServiceCallStageCard.SetStatestgtrno2k2u0o0000k' +
                                             'ruvf5gospqohlo"]').get_attribute("href").split("?")[-1]
    link_resource = driver.find_element_by_xpath('//*[@id="Resources"]').get_attribute("href").split("8080")[-1]
    link_request = "http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?" + link_request
    link_take = "http://sdn.pilot.ru:8080/fx/$guic/ru.naumen.guic.components.forms.form_jsp?" + link_take
    link_resource = "http://sdn.pilot.ru:8080" + link_resource
    number = driver.find_element_by_xpath('//*[@id="title_td"]').text
    register_requests.update({shop: number})
    time.sleep(0.5)
    # driver.get(link_take)
    time.sleep(0.5)
    #  driver.find_element_by_id("ok").click()
    time.sleep(1)
    driver.get(link_resource)

    link_add_resource = driver.find_element_by_xpath('//*[@id="Resources.ServiceCallResourcesList.ServiceCallResou' +
                                                     'rcesListActionContainer.ObjectListReport.tableListAndButtons.' +
                                                     'ServiceCallResourcesListServiceCallResourcesList.SetRelationWi' +
                                                     'zard"]').get_attribute("href").split("8080")[-1]
    link_add_resource = "http://sdn.pilot.ru:8080" + link_add_resource
    driver.get(link_add_resource)

    """Добавить серийные номера"""
    serial_numbers = [sn.split("_")[0] for sn in serial_numbers.split()]
    for sn in serial_numbers:
        create_list_kkt.enter_words("invNumberSearchString", sn)
        driver.find_element_by_id('invNumberSearchRB').click()
        driver.find_element_by_xpath('//*[@id="Resources.ServiceCallResourcesList.ServiceCallResourcesListActionConta' +
                                     'iner.ObjectListReport.tableListAndButtons.ServiceCallResourcesListServiceCallRe' +
                                     'sourcesList.SetRelationWizard.tableContainer.SearchResultsListParent.SearchResu' +
                                     'ltsList.selectedObjects__chkbox"]').click()
        driver.find_element_by_xpath('//*[@id="add"]/img').click()
    driver.find_element_by_id("next").click()

    driver.get(link_request)

    link_change_type = driver.find_element_by_xpath('//*[@id="ServiceCall.ServiceCallCard.SetServiceCallCase"]'
                                                    ).get_attribute("href").split("8080")[-1]
    link_change_type = "http://sdn.pilot.ru:8080" + link_change_type
    driver.get(link_change_type)

    xpath_restore = '//*[@id="case"]/option[@nonshifted="Восстановление работоспособности"]'
    driver.find_element_by_xpath(xpath_restore).click()
    time.sleep(0.3)
    xpath_category_fn = '//*[@id="valuefabasefs000080000kcn652egnnr2opk"]/option[@nonshifted="ККТ: Замена ФН"]'
    driver.find_element_by_xpath(xpath_category_fn).click()
    time.sleep(0.1)
    driver.find_element_by_xpath('//*[@id="edit"]').click()
    driver.get(link_request)

    time.sleep(1)


def main():
    contact_human = input("Введите контактное лицо в формате ФАМИЛИЯ ИМЯ ДОЛЖНОСТЬ\n")
    contact_phone = input("Введите контактный НОМЕР ТЕЛЕФОНА в без лишний символов, пожалуйста\n")
    contact_email = input("Введите контактный EMAIL формата test@test.ru\n")
    """
    contact_human = 'Владислав Войков Департамент ИТ- Аутсорсинга'
    contact_phone = "+7 (495) 734-9137"
    contact_email = "support@5-55.ru"
    """
    count = 0
    with open("lets_do_this.csv", "r") as file:
        for line in file:
            shop = line.split(";")[0]
            serial_numbers = line.split(";")[1]
            if shop.startswith("\""):
                shop = str(shop)[1:-1].replace("\"\"", "\"")
            find_shop(shop)
            try:
                create_request(serial_numbers, contact_human, contact_phone, contact_email)
                add_kkt_and_register(serial_numbers, shop)
            except:  # NoSuchElementException
                bad_not_service.update({shop: serial_numbers})
            count += 1
            print(count, "заявок зарегистрировано")
    dict_files = {"bad_not_service.csv": bad_not_service,
                  "зарегистрированные_заявки.csv": register_requests}
    for path, dictionary in dict_files.items():
        create_list_kkt.record_files(path, dictionary)


if __name__ == '__main__':
    main()
