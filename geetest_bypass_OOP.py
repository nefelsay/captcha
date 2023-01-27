import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from func_disatance import get_distance_to_center
from selenium import webdriver


class Slider():
    def __init__(self):
        self.proxy = {'proxy': {
            'http': "socks5://wRKZPG:snFyfD@91.229.113.96:8000",
            'https': "socks5://wRKZPG:snFyfD@91.229.113.96:8000",
        }}
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.action = ActionChains(self.browser)
        self.url = 'https://captcha-parsinger.ru/geetest?page=3'
        self.list_disance = []
        self.distance = int()

    def slide_puzle(self, slider_arrow):
        num1 = self.distance // 100
        self.list_disance.extend(num1 * [100])
        num2 = self.distance % 100
        self.list_disance.append(num2)

        print(f"Общая дистанция {self.distance}")
        print(f"Число distance разбитое на части {self.list_disance}")
        print(f"Проверка правильности разделения {sum(self.list_disance)}")

        self.action.click_and_hold(slider_arrow).perform()
        for x in self.list_disance:
            self.action.move_by_offset(xoffset=x, yoffset=0).pause(3).perform()

        self.action.release().perform()
        print('Движение завершено')
        time.sleep(10)

    def main(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)
        self.browser.find_element(By.CLASS_NAME, 'geetest_radar_tip').click()
        background = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'canvas[class="geetest_canvas_bg geetest_absolute"]')))
        if background:
            time.sleep(3)
            background.screenshot('background.png')
        self.distance = round(get_distance_to_center('background.png')) - 26
        slider_arrow = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        self.slide_puzle(slider_arrow)

        #Получает вебэлемент кнопки Network failure
        network_failure = self.browser.find_element(By.CLASS_NAME, 'geetest_reset_tip_content')
        #Ожидаем пока она станет кликабельной и кликаем по ней.
        if self.wait.until(EC.element_to_be_clickable(network_failure)):
            network_failure.click()
            # Очищаем дистанцию
            self.distance = 0
            self.list_disance.clear()

            self.main()
            self.slide_puzle(slider_arrow)
        time.sleep(1)
        self.browser.quit()


if __name__ == '__main__':
    slider = Slider()
    slider.main()
