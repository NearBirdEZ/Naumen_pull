import create_list_kkt

pull_kkt_count = {}  # словарь для снегерированного списка
shop_count = {}  # словарь для подготовленного файла
gg = {}  # Чистейшие, как самогон моего деда ККТ, для последующего заведения
bg = {}  # В одном шаге от заведения ккт, но нет


def row_clear(line):
    """Функция для очистки каждой строки от двойных ковычек, а так же
    приведение каждой строки к прописному виду для последующего сравнения"""
    if line.startswith("\""):
        line = line[1:-1].replace("\"\"", "\"")
    return line.lower()


def main():
    """Заполенние словаря pull_kkt_count значениями вида 'МАГАЗИН' : КОЛИЧЕСТВО ККТ.
    Данные используются из СГЕНЕРИРОВАННОГО СПИСКА по поиску ккт для последующего сравнения"""
    for key, value in create_list_kkt.owners_kkt.items():
        pull_kkt_count[key] = len(value)

    """Заполенние словаря pull_kkt_count значениями вида 'МАГАЗИН' : КОЛИЧЕСТВО ККТ. 
    Данные используются из ПРЕДОСТАВЛЕННОГО СПИСКА вида 1 МАГАЗИН - 1 ККТ для последующего сравнения"""
    with open("shops.txt", "r", encoding="utf-8") as file:
        for row in file:
            row = row.lower().strip()
            shop_count[row] = shop_count.get(row, 0) + 1

    """В связи с тем, что словарь, который был сгенерирован по ккт отражает что на 
    данный момент есть в Naumen'e, поэтому магазин/значение берется из него
    Если такой магазин есть в shop_count, происходит сравнение колиества заявленного ккт и найденного (по поиску"""
    for key, value in pull_kkt_count.items():
        """Не попадают, если в подготовленном файле нет магазина (НД) или 
        некоторые ККТ не заведены на необходимом магазине"""
        key = key.lower()
        if shop_count.get(key) == value:
            gg.update({key: create_list_kkt.owners_kkt[key]})
        else:
            bg.update({key: value})
    create_list_kkt.record_files("lets_do_this.csv", gg)
    create_list_kkt.record_files("bad_requests.csv", bg)


if __name__ == '__main__':
    main()
