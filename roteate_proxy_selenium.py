#https://stepik.org/a/104774
import itertools
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from seleniumwire import webdriver as wire_webdriver

class ProxyRotator:
    def __init__(self, proxies):
        # создает итератор, который будет перебирать прокси-сервера в цикле
        self.proxies = itertools.cycle(proxies)
        # хранит текущий используемый прокси-сервер
        self.current_proxy = None
        self.good_proxy = {}
        # счетчик запросов, для определения когда нужно сменить прокси-сервер
        self.request_counter = 0

    def change_proxy(self):
        # меняет текущий используемый прокси-сервер на следующий в списке
        self.current_proxy = next(self.proxies)
        # сбрасывает счетчик запросов
        self.request_counter = 0
        return self.current_proxy

    def get_proxy(self):
        # проверяет нужно ли сменить пр
        # проверяет нужно ли сменить прокси-сервер
        if self.request_counter % 1 == 0:
            self.change_proxy()
        # увеличивает счетчик запросов
        self.request_counter += 1
        return self.current_proxy

proxies = [
    {'http': "socks5://3QLrMH:efE58u@194.67.201.65:9282", 'https': "socks5://3QLrMH:efE58u@194.67.201.65:9282"},
    {'http': "socks5://Y8XABo:JWeAHQ@194.67.223.202:9365", 'https': "socks5://Y8XABo:JWeAHQ@194.67.223.202:9365"},
    {'http': "socks5://4bL6Jn:SEKwVS@196.18.167.105:8000", 'https': "socks5://4bL6Jn:SEKwVS@196.18.167.105:8000"},
    {'http': "socks5://wRKZPG:snFyfD@91.229.113.96:8000", 'https': "socks5://wRKZPG:snFyfD@91.229.113.96:8000"}
]

proxy_rotator = ProxyRotator(proxies)

while True:
    proxy = proxy_rotator.get_proxy()
    print(f'using proxy: {proxy}')
    prx = {}
    prx.update({'proxy': proxy})
    with wire_webdriver.Chrome(seleniumwire_options=prx) as browser:
        browser.get("http://httpbin.org/ip")
        print(browser.find_element(By.TAG_NAME, 'body').text)
        time.sleep(2)
        browser.quit()
