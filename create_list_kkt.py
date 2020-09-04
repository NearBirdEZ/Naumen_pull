import csv
from main_def import driver
from selenium.common.exceptions import NoSuchElementException
import time
import os

kkt_not_attached = {}  # ККТ, которые не привязаны ни к одному магазину / флаг 1
deleted_owners = {}  # Магазины с префиксом УДАЛЕН / флаг 2
kkt_p = {}  # ККТ с префиксом (Р) / флаг 3  НЕ ИСПОЛЬЗУЕТСЯ
owners_kkt = {}  # Адрес и ККТ для заведения пула / флаг 4
kkt_has_two_owners = {}  # ККТ, которые имеют два или более владельцев / флаг 5
doubles_kkt = {}  # В системе имеется более одного ККТ с таким же номером / флаг 6
dict_files = {"bad_ККТ_без_привязки.csv": kkt_not_attached,
              "bad_Магазины_с_префиксом_удален.csv": deleted_owners,
              "bad_ККТ_с_префиксом_(Р).csv": kkt_p,
              "ККТ_для_заведения_пула.csv": owners_kkt,
              "bad_ККТ_с_двумя_или_более_владельцами.csv": kkt_has_two_owners,
              "bad_У_ККТ_есть_дубли.csv": doubles_kkt}


def enter_words(id_object, words, t=0.5):
    """Функция для заполнения полей по ID"""
    driver.find_element_by_id(id_object).clear()
    driver.find_element_by_id(id_object).send_keys(words)
    time.sleep(t)


def find_search(serial_number):
    """Функция поиска по заявке
    СДелать полиморфной
    """
    index_url = "http://sdn.pilot.ru:8080/fx/sd/ru.naumen.sd.published_jsp?uuid=corebofs000080000ikhm8pnur5l85oc"
    driver.get(index_url)
    enter_words("sdsearch_CMDBObjectInvNumberSearchTypeCMDBObjectAdvSearch", serial_number)
    driver.find_element_by_id("dosearchsdsearch_CMDBObjectInvNumberSearchTypeCMDBObjectAdvSearch").click()


def parser_owners(serial_number):
    """Получение владельцев ККТ"""
    time.sleep(1)
    try:
        owners = driver.find_element_by_id("owners").text
        owners = owners.lower()
        if owners == "":
            return 1, 0, serial_number

        elif len(owners.split("\n")) == 1 and owners.startswith("удален_"):
            return 2, owners, serial_number

        # ИГНОРИРОВАНИЕ СЕРИЙНИКОВ С ПРЕФИКСОМ (Р)
        # elif len(owners.split("\n")) == 1 and ("(P)" in driver.find_element_by_id("title_td").text):
        #    return 3, owners, serial_number

        elif len(owners.split("\n")) == 1:
            return 4, owners, serial_number

        elif len(owners.split("\n")) > 1:
            return 5, owners, serial_number

    except NoSuchElementException:
        return 6, 0, serial_number


def append_dict(owner: str, serial_number: str, dictionary: dict):
    if dictionary.get(owner):
        dictionary[owner].append(serial_number)

    else:
        dictionary[owner] = [serial_number]


def record_lst(serial_number, end_date):
    flag, owner, serial_number = parser_owners(serial_number)
    serial_number = serial_number.strip() + "_" + end_date

    if flag == 1:
        append_dict(owner, serial_number, kkt_not_attached)
    elif flag == 2:
        append_dict(owner, serial_number, deleted_owners)
    # ИГНОРИРОВАНИЕ СЕРИЙНИКОВ С ПРЕФИКСОМ (Р)
    # elif flag == 3:
    # append_dict(owner, serial_number, kkt_p)
    elif flag == 4:
        append_dict(owner, serial_number, owners_kkt)
    elif flag == 5:
        append_dict(owner, serial_number, kkt_has_two_owners)
    elif flag == 6:
        append_dict(owner, serial_number, doubles_kkt)


def record_files(path, dictionary):
    if path.startswith("bad"):
        try:
            os.mkdir("problems_requests")
        except FileExistsError:
            pass
        os.chdir("problems_requests")
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=';')
        for key, value in dictionary.items():
            value = str(value)[1:-1].replace("\'", "").replace(",", "")
            writer.writerow([key, value])
    if path.startswith("bad"):
        os.chdir("..")


def main():
    count = 1
    with open("kkt.txt", "r") as f:
        total_line = sum(1 for _ in f)
    with open("kkt.txt", "r") as f:
        for row in f:
            serial_number, end_date, *_ = row.split()
            find_search(serial_number)
            record_lst(serial_number, end_date)
            print(
                f"Завершено на {round((count / total_line) * 100, 1)} процентов или по-русски {count} из {total_line} ККТ")
            count += 1

    for path, dictionary in dict_files.items():
        if len(dictionary) > 0:
            record_files(path, dictionary)


if __name__ == '__main__':
    main()
