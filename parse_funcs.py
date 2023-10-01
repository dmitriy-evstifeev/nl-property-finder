from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def _wait_get_elem(driver_, xpath_, timeout_):
    return WebDriverWait(driver_, timeout_).until(
        EC.presence_of_element_located((By.XPATH, xpath_))
    )


def _get_elem_attributes(driver_, wait_for_load_, url_xpath_, status_xpath_=None, timeout_=10):
    if wait_for_load_:
        url_elem = _wait_get_elem(driver_, url_xpath_, timeout_)
    else:
        url_elem = driver_.find_element(By.XPATH, url_xpath_)
    url_ = url_elem.get_attribute('href')

    if status_xpath_:
        try:
            status_ = driver_.find_element(By.XPATH, status_xpath_).get_attribute('innerText')
        except NoSuchElementException:
            status_ = 'Available'
    else:
        status_ = None
    return url_, status_


def mvgm_parse(web_driver):
    urls = []
    xpath_root = "//ul[@id='search-results']/li[{}]/div[1]/div"
    last_page = False
    wait_for_load = True
    i = 1
    while True:
        try:
            url, status = _get_elem_attributes(
                driver_=web_driver, wait_for_load_=wait_for_load,
                url_xpath_=f'{xpath_root.format(i)}/a',
                status_xpath_=f'{xpath_root.format(i)}/figure/span'
            )
            wait_for_load = False
        except NoSuchElementException:
            break

        if status not in ('Available', 'Nieuw'):
            last_page = True
            break

        urls.append(url)
        i += 1
    return urls, last_page


def vesteda_parse(web_driver):
    urls = []
    xpath = "//ul[@class='o-layout u-margin-bottom-none' and @data-cy='unit-search-results-list']/li[{}]/div/a"
    wait_for_load = True
    i = 1
    while True:
        try:
            url, status = _get_elem_attributes(
                driver_=web_driver, wait_for_load_=wait_for_load,
                url_xpath_=xpath.format(i),
                status_xpath_=f'{xpath.format(i)}/article/div[1]/span'
            )
            wait_for_load = False
        except NoSuchElementException:
            break

        if status.startswith('Re'):  # Reserved, Rented, Rented with reservation
            break

        urls.append(url)
        i += 1
    return urls, True


def rebo_parse(web_driver):
    urls = []
    xpath = "//div[@class='row js-object-items']/div/div[{}]/div/a"
    wait_for_load = True
    for i in range(1, 51):  # Should be more than enough
        try:
            url, _ = _get_elem_attributes(
                driver_=web_driver, wait_for_load_=wait_for_load,
                url_xpath_=xpath.format(i)
            )
            wait_for_load = False
        except NoSuchElementException:
            break
        urls.append(url)
    return urls, True


def bouwinvest_parse(web_driver):
    urls = []
    xpath = "//div[@class='projects-wrap bg-background-grey']/a[{}]"
    last_page = False
    wait_for_load = True
    i = 1
    while True:
        try:
            url, status = _get_elem_attributes(
                driver_=web_driver, wait_for_load_=wait_for_load,
                url_xpath_=xpath.format(i),
                status_xpath_=f'{xpath.format(i)}/span/span[1]/span/span[4]',
                timeout_=5
            )
            wait_for_load = False
        except NoSuchElementException:
            break
        except TimeoutException:
            last_page = True
            break

        if status == 'Available' or 'beschikbaar' in status.lower():
            urls.append(url)
        i += 1
    return urls, last_page


def schep_parse(web_driver):
    urls = []

    # Handling endless page loop
    # cur_page = int(web_driver.current_url.split('=')[-1])
    # if cur_page > 1:
    #     prev_page_url = _wait_get_elem(web_driver, "//a[@id='Main_ctl01_PrevLink']").get_attribute('href')
    #     prev_page = int(prev_page_url.split('/')[-1])
    #     if (cur_page - prev_page) > 1:
    #         return urls, True

    xpath = "//div[@class='woningList clearer row']/a[{}]"
    last_page = False
    wait_for_load = True
    i = 1
    while True:
        try:
            url, status = _get_elem_attributes(
                driver_=web_driver, wait_for_load_=wait_for_load,
                url_xpath_=xpath.format(i),
                status_xpath_=f'{xpath.format(i)}/div[1]/span'
            )
            wait_for_load = False
        except NoSuchElementException:
            break

        if status.lower() not in ('available', 'beschikbaar', 'nieuw'):
            last_page = True
            break

        urls.append(url)
        i += 1
    return urls, last_page
