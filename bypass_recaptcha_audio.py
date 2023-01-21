#https://stepik.org/a/104774
import pydub
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from seleniumwire import webdriver
from fake_useragent import UserAgent
import speech_recognition as sr
from selenium.webdriver import Keys


prx_1 = {'proxy': {
    'http': "socks5://wRKZPG:snFyfD@91.229.113.96:8000",
    'https': "socks5://wRKZPG:snFyfD@91.229.113.96:8000",
    }}
prx_2 = {'proxy': {
    'http': "socks5://Y8XABo:JWeAHQ@194.67.223.202:9365",
    'https': "socks5://Y8XABo:JWeAHQ@194.67.223.202:9365",
}}
name_audio_file = 'audio_file.mp3'
def write_audio(url):
    response = requests.get(url)
    with open(f'{name_audio_file}', 'wb') as file:
        file.write(response.content)

def audio_to_text():
    with open(f'{name_audio_file}.mp3', 'wb') as files:
        path_to_mp3 = name_audio_file
        path_to_wav = 'audio_file_wav.wav'
        sound = pydub.AudioSegment.from_file(path_to_mp3, 'mp3')
        sound.export(path_to_wav, format="wav")
        sample_audio = sr.AudioFile(path_to_wav)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        key = r.recognize_google(audio)
        return key

def main():
    ua = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={ua}")
    with webdriver.Chrome(chrome_options=options, seleniumwire_options=prx_2) as browser:
        browser.get('https://captcha-parsinger.ru/v2?page=3')
        browser.implicitly_wait(10)
        frames = browser.find_elements(By.TAG_NAME, "iframe")

        # #переключение на iframe капчи
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='reCAPTCHA']")))

        # #клик по чекбоксу капчи
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]'))).click()
        browser.implicitly_wait(10)

        # возвращаемся к основному контексту веб-страницы.
        browser.switch_to.default_content()

        #Ожидаем доступность iframe и кликаем по готовности
        #iframe с набором картинок
        WebDriverWait(browser, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, f"iframe[title='текущую проверку reCAPTCHA можно пройти в течение ещё двух минут']")))

        # Ожидаем кликабельность кнопки с аудио
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-audio-button"]'))).click()

        #Находим тег аудио по ID и излекаем содержимое атрибута src
        src = browser.find_element(By.ID, "audio-source").get_attribute("src")
        print(f"[INFO] Audio src: {src}")
        write_audio(src)


        browser.find_element(By.CSS_SELECTOR, 'input[id="audio-response"]').send_keys(audio_to_text().lower())
        browser.find_element(By.ID,"audio-response").send_keys(Keys.ENTER)
        time.sleep(10)
if __name__ == '__main__':
    main()
