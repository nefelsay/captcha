import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


def main():
    with webdriver.Chrome() as browser:
        browser.get('https://captcha-parsinger.ru/v2?page=3')
        browser.implicitly_wait(10)
        frames = browser.find_elements(By.TAG_NAME, "iframe")

        #Ожидаем доступность iframe и кликаем по готовности
        #iframe с чек боксом
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='reCAPTCHA']")))

        #клик по чекбоксу капчи внутри iframe
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'recaptcha-anchor'))).click()

        browser.implicitly_wait(10)
        #возвращаемся к основному контексту веб-страницы.
        browser.switch_to.default_content()

        #Ожидаем доступность iframe и кликаем по готовности
        #iframe с набором картинок
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='текущую проверку reCAPTCHA можно пройти в течение ещё двух минут']")))

        #Ожидаем кликабельность кнопки с аудио
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'recaptcha-audio-button'))).click()

        #Находит тег аудио по ID и излекаем содержимое атрибута src
        src = browser.find_element(By.ID, "audio-source").get_attribute("src")
        print(f"[INFO] Audio src: {src}")

        time.sleep(5)

if __name__ == '__main__':
    main()
