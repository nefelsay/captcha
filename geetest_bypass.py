#https://stepik.org/a/104774

import time
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from func_disatance import get_distance_to_center


def main():
    prxoxy = {'proxy': {
        'http': "socks5://wRKZPG:snFyfD@91.229.113.96:8000",
        'https': "socks5://wRKZPG:snFyfD@91.229.113.96:8000",
    }}
    with uc.Chrome(version_main=109, seleniumwire_options=prxoxy) as browser:
        url = f'https://captcha-parsinger.ru/geetest?page=3'
        browser.get(url)

        browser.implicitly_wait(10)
        # Кликаем на чекбокс.
        browser.find_element(By.CLASS_NAME, 'geetest_radar_tip').click()

        # Дожидаемся появления тега canvas.
        background = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'canvas[class="geetest_canvas_bg geetest_absolute"]')))
        # Если тег появился, то делаем скриншот.
        if background:
            time.sleep(2)
            # т.к. невозможно дождаться появления содержимого canvas через неявные ожинаия, ставим простой слип, 2 секунды хватает.
            # Если мы не используем простой слип, то скриншот может быть сделан на пару мнгновений раньше необходимого, и дистанция не будет рассчитана.
            # Делаем скриншот облсти капчи который лежит в теге canvas
            background.screenshot('background.png')



        # distance - расстояние которое нужно пройти пазлу, где -26 это расстояние в px от левого края до центра стартового пазла.
        # Передаём в функцию get_distance_to_center() путь к скриншоту который делали ранее.
        # Используем встроенную функцию round() для округения числа, потому что нейросеть возвращает дробное число.
        distance = round(get_distance_to_center('background.png')) - 26

        # Ожидаем появление слайдера
        slider = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))



        # lst - список с числами которые мы наполняем чтобы итерироваться по нему и двигать пазл.
        # например если distance= 168, список lst будет состоять из двух чисел 100 и 68.
        # Если distance= 210 список lst будет состоять из трёх чисел 100, 100 и 10.
        # Это нужно для имитации движения человеком. Переместить пазл с 0 до 210 можно, но капча может не принять такое поведение.
        lst = []

        # Следующие 4 строки выполняют операции над distance и наполняет список lst нобходимымы числами.
        num1 = distance // 100
        lst.extend(num1 * [100])
        num2 = distance % 100
        lst.append(num2)

        # Принты для наглядности.
        print(f"Общая дистанция {distance}")
        print(f"Число distance разбитое на части {lst}")
        print(f"Проверка правильности разделения {sum(lst)}")

        # Создаём экземпляр класса ActionChains, для дальнейшего использования.
        action = ActionChains(browser)

        # Если slider появился, то заходим в условие.
        if slider:
            # Нажимаем и держим слайдер.
            action.click_and_hold(slider).perform()

            for x in lst:
                # Двигаем slider по оси X с рандомной задержкой.
                action.move_by_offset(xoffset=x, yoffset=0).pause(random.random() * 3).perform()
            action.release().perform()
            print('Движение завершенно')
            time.sleep(10)


if __name__ == '__main__':
    main()
