from selenium import webdriver
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha


solver = TwoCaptcha('***********API code***********')
img_name = 'img.png'
def sender_solve(path=img_name):
    print('2) Изображение отправленно для разгадывания:')
    result = solver.normal(path)
    print('3) От API пришёл ответ: ', result)
    #Функция вернёт словарь {'captchaId': '72447681441', 'code': 'gbkd'}
    return result


with webdriver.Chrome() as browser:
    browser.get('https://captcha-parsinger.ru/?page=3')
    browser.implicitly_wait(10)

    if 'Подтвердите, что вы не робот' in browser.page_source:
        browser.find_element(By.CSS_SELECTOR, 'div[class="chakra-form-control css-1sx6owr"]').find_element(By.TAG_NAME,'img').screenshot(img_name)
        print('1) Скриншот области успешно сделан')
        func_sender_solve = sender_solve(img_name)
        browser.find_element(By.ID, 'field-:r0:').send_keys(func_sender_solve['code'])
        browser.find_element(By.CSS_SELECTOR, 'button[class="chakra-button css-1wq39mj"]').click()
        #Запускаем бесконечный цикл на случай если неудачных попыток будет несколько.
        while True:
            #Пытаемся спарсить список товаров
            name_card = [x.text for x in browser.find_elements(By.CLASS_NAME, 'css-5ev4sb')]
            #Если спарсить не получилось, и список name_card не содержит элементов то переходит в блок else
            if len(name_card) > 0:
                #Репортим о успешном решении
                solver.report(func_sender_solve['captchaId'], True)
                print("Отправлен репорт о успешном разгадывании")
                print('4)',name_card)
                #После успешного получения данных, прерываем цикл
                break
            else:
                print("Капча решена не верно, повторяем попытку")
                #Репортим о неудачной попытки разагадать капчу
                solver.report(func_sender_solve['captchaId'], False)
                #Делаем новый скриншот, т.к. после неуспешной попытке капча обновилась
                print('Повторный скриншот области')
                browser.find_element(By.CSS_SELECTOR, 'div[class="chakra-form-control css-1sx6owr"]').find_element(
                    By.TAG_NAME, 'img').screenshot('img.png')
                #Отправляем скриншот повторно
                browser.find_element(By.ID, 'field-:r0:').send_keys(func_sender_solve['code'])
                #Кликаем по нопку повторно
                browser.find_element(By.CSS_SELECTOR, 'button[class="chakra-button css-1wq39mj"]').click()
                #Пытаемся наполнить список name_card найденными элементами
                [name_card.append(x.text) for x in browser.find_elements(By.CLASS_NAME, 'css-5ev4sb')]
