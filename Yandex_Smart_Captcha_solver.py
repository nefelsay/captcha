#https://stepik.org/a/104774

import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from twocaptcha import TwoCaptcha

dict_resut = {}

#Функция принимает путь к изображению, отправляет в API 2captcha и возвращает словарь со словом
def sender_solve(path):
    solver = TwoCaptcha('*********************')
    print('2) Изображение отправленно для разгадывания:')
    result = solver.normal(path,
                           param='ru')
    print('3) От API пришёл ответ: ', result)
    #API вернёт словарь {'captchaId': '72447681441', 'code': 'gbkd'}
    #Обновляем словарь для дальнейшего извлечения ID капчи и отправки репорта
    dict_resut.update(result)
    return result['code']

def main():
    ua = UserAgent()
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('user-data-dir=C:\\User_Data')
    options_chrome.add_argument(f"--user-agent={ua}")
    with webdriver.Chrome(options=options_chrome) as browser:
        browser.implicitly_wait(15)
        url = f'https://captcha-parsinger.ru/yandex?page=3'
        browser.get(url)
        #Переключаемся на iframe капчи
        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='SmartCaptcha checkbox widget']")))

        #Ожидаем кнопку и кликаем по ней
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[class="CheckboxCaptcha-Button"]'))).click()

        #Возвращаемся к основному коду на странице
        browser.switch_to.default_content()

        #Переключаемся на новый iframe с картинкой
        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='SmartCaptcha advanced widget']")))

        #Хардкодим имя картинки
        img_names = 'img_yandex.png'
        with open(img_names, 'wb') as file:
            #Извлекаем атрибут src из тега в котором хранится ссылка на изображение
            img = browser.find_element(By.CSS_SELECTOR, 'img[class="AdvancedCaptcha-Image"]').get_attribute('src')
            #Делаем простой requests запрос для скачивания картинки и её записи в файл
            file.write(requests.get(img).content)
            print(f'1) url image: {img}')

        sender_solve(img_names)
        print(f'4) {dict_resut["code"]}')
        #Вставлям необходимую часть словаря dict_resut в котором лежит разгаданное слова с капчи
        browser.find_element(By.CSS_SELECTOR, 'input[class="Textinput-Control"]').send_keys(dict_resut['code'])
        
        #Возвращаемся к основному коду на странице, для извлечения артикулов
        browser.switch_to.default_content()
        
        #Кликаем на кнопку отправить
        browser.find_element(By.CSS_SELECTOR, 'button[class="CaptchaButton CaptchaButton_view_action"]').click()

        #10 секунд наслаждаемся результатом =)
        time.sleep(10)


if __name__ == '__main__':
    main()
