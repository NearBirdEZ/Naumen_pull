from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import create_list_kkt
from config import log, pas
import time


driver = webdriver.Chrome(ChromeDriverManager().install())


def start_naumen():
    """Функция старта наумена"""
    url = "http://sdn.pilot.ru:8080/fx"
    driver.get(url)
    time.sleep(0.5)
    create_list_kkt.enter_words('login', log)
    create_list_kkt.enter_words("password", pas)
    driver.find_element_by_name('LogonFormSubmit').click()
    time.sleep(1)
