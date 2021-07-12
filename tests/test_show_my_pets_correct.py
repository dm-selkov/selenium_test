import pytest
from selenium import webdriver
from settings import valid_email, valid_password, user_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True, scope='session')
def testing():
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('http://petfriends1.herokuapp.com/login')

    yield driver

    driver.quit()


def test_show_my_pets_correct(testing):
    wait = WebDriverWait(testing, 10)
    wait.until(EC.title_is('PetFriends: Login'))

    email_form = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_form.send_keys(valid_email)
    pass_form = wait.until(EC.visibility_of_element_located((By.ID, 'pass')))
    pass_form.send_keys(valid_password)
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    submit_button.click()
    page_head = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
    assert page_head.text == 'PetFriends'

    my_pets_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/my_pets"]')))
    my_pets_button.click()
    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class=".col-sm-4 left"]/h2'), user_name))

    # достаем из статистики юзера количество питомцев
    # согласен, способ кривой и сильно зависит от верстки, но другого не придумал
    user_stats = testing.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text
    # делим результат на строки, из строки с количеством питомцев берем количество
    number_of_pets_stat = int(user_stats.split('\n')[1].split(' ')[1])

    # смотрим количество строк в таблице с питомцами и сравниваем со статистикой
    # animals = testing.find_elements_by_xpath('//div[@id="all_my_pets"]//tbody/tr')
    animals = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//tbody/tr')))
    assert number_of_pets_stat == len(animals)

    images = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//img')))

    names = []
    types = []
    ages = []
    for animal in animals:
        names.append(animal.find_elements_by_tag_name('td')[0].text)
        types.append(animal.find_elements_by_tag_name('td')[1].text)
        ages.append(animal.find_elements_by_tag_name('td')[2].text)

    assert len(names) == len(animals)
    for name in names:
        assert name != ''

    assert len(types) == len(animals)
    for type in types:
        assert type != ''

    assert len(ages) == len(animals)
    for age in ages:
        assert age != ''
        try:
            int(age)
        except ValueError:
            print('Возраст должен быть указан числом')

    set_names = set(names)
    assert len(names) == len(set_names)

    assert len(images) >= len(animals) / 2
