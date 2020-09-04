from create_request import find_shop, NoSuchElementException, driver
from create_list_kkt import record_files
from create_list_kkt import main as mn

wet_shop = []
bad_dry_shop = {}


def main():
    with open("wet_shops.txt", "r") as file:
        total_line = sum(1 for _ in file)
        count = 0
        with open("wet_shops.txt", "r") as file:
            for shop in file:
                shop = shop.strip()
                find_shop(shop)
                try:
                    title_shop = driver.find_element_by_xpath(
                        '//*[@id="ServiceCallRegistrationNew.RegForm.MainContainer' +
                        '.LeftColumn.clientProperties.title"]/a').text.lower()
                    if title_shop.startswith("дубль"):
                        bad_dry_shop[title_shop] = bad_dry_shop.get(title_shop, 0) + 1
                    else:
                        wet_shop.append(title_shop)
                except NoSuchElementException:
                    bad_dry_shop[shop] = bad_dry_shop.get(shop, 0) + 1
                count += 1
                print(
                    f"Завершено на {round((count / total_line) * 100, 1)} процентов или по-русски {count} из {total_line} магазинов")
    record_files("bad_cant_find_shops.csv", bad_dry_shop)
    with open("shops.txt", "w", encoding="utf-8") as file:
        for line in wet_shop:
            file.write(line + "\n")


if __name__ == '__main__':
    main()
