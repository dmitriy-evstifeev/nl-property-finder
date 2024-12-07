import re
from os import environ

from selenium.webdriver.common.by import By


def parse_mvgm(soup):
    urls = []
    for offer in soup.find_all(
        class_='card card-woning shadow-sm rounded-5 rounded-end-0 rounded-bottom-0 overflow-hidden flex-grow-1'
    ):
        status = offer.find(class_=re.compile("status-dot bg-status")).next_sibling.strip()
        if status != 'Te huur':
            last_page = True
            break

        href = offer.find(class_='stretched-link')['href']
        if href.startswith('https://wonenbijbouwinvest'):
            continue

        city_elem = offer.find(class_='card-title h5 text-secondary mb-0').next_sibling.next_sibling
        city = ' '.join(city_elem.text.split()[1:]) if city_elem else 'Unknown'

        price_elem = offer.find(class_='fw-bold')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None
        
        urls.append((f'https://ikwilhuren.nu{href}', city, price))
    else:
        last_page = not len(urls)
    return urls, last_page


def parse_vesteda(soup):
    urls = []
    for offer in soup.find_all(class_='o-card--listview-container'):
        status = offer.find(class_=re.compile('c-object-label c-object-label'))
        if status:
            break

        href = offer.next_element['href']

        city_elem = offer.find(class_='u-heading u-margin-bottom-none')
        city = city_elem.text.strip() if city_elem else 'Unknown'

        price_elem = offer.find(class_='h5')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((f'https://www.vesteda.com{href}', city, price))
    return urls, True


def login_rebo(web_driver):
    web_driver.get('https://rebowonenhuur.nl/login/')
    login_field = web_driver.find_element(By.XPATH, '//input[@name="txtEmail"]')
    login_field.send_keys(environ['REBO_LOGIN'])
    password_field = web_driver.find_element(By.XPATH, '//input[@name="txtWachtwoord"]')
    password_field.send_keys(environ['REBO_PWD'])
    login_button = web_driver.find_element(By.XPATH, '//button[@class="btn btn-secondary btn-block"]')
    login_button.click()


def parse_rebo(soup):
    urls = []
    for offer in soup.find_all(class_='card card-result-list mb-4'):
        status = offer.find('span').text
        if status != 'Te huur':
            break

        href = offer.find('a').attrs.get('href')
        if href:
            city_elem = offer.find(class_='card-text')
            city = city_elem.text if city_elem else 'Unknown'

            price_elem = offer.find(class_='value ml-1')
            price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

            urls.append((f'https://rebowonenhuur.nl{href}', city, price))
    return urls, True


# With status checking: doesn't work correctly without Selenium. Dynamically updates statuses
# ===========
def parse_bouwinvest(soup):
    urls = []
    offers = soup.find_all(class_='projectproperty-tile box-shadow')
    for offer in offers:
        status = soup.find(class_='sticker-bar sticker-bar__top').next_element
        if not 'beschikbaar' in status.lower():
            continue

        url = offer.find('a').attrs.get('href')

        city_elem = offer.find(class_='paragraph fw-light')
        city = city_elem.text if city_elem else 'Unknown'
        
        price_elem = offer.find(class_='price-tag')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((url, city, price))

    next_page_address = soup \
        .find(class_=re.compile('active active-exact pagination__arrow pagination__next icon-caret-right')) \
        .attrs.get('class')
    is_last_page = 'disabled' in next_page_address
    return urls, is_last_page


def parse_schep(soup):
    urls = []
    for offer in soup.find_all(class_='object col-xs-12'):
        status = offer.find('span').text
        if status in ('Onder optie', 'Verhuurd ovb', 'Verhuurd'):
            last_page = True
            break

        href = offer['href']
        if href.startswith('https://wonenbijbouwinvest'):
            continue

        city_elem = offer.find(class_='plaats')
        city = city_elem.text if city_elem else 'Unknown'

        price_elem = offer.find(class_='prijs')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((f'https://zoeken.schepvastgoedmanagers.nl{href}', city, price))
    else:
        last_page = not len(urls)
    return urls, last_page


def parse_stienstra(soup):
    urls = []
    for offer in soup.find_all(class_='property-item table-list order-2'):
        status = offer.find('span', class_='label-status label label-default').text
        if status != 'Te huur':
            continue

        object = offer.find('h2', class_='property-title').a

        href = object.attrs['href']
        city = object.text.split()[-1]

        price_elem = offer.find(class_='item-price')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((f'https://www.stienstra.nl{href}', city, price))
    last_page = not len(urls)
    return urls, last_page
    

def parse_vanderlinden(soup):
    urls = []
    for offer in soup.find_all(class_='zoekresultaat zoekresultaat3kol'):
        status = offer.span.text
        if status not in ('Direct beschikbaar', 'Binnenkort beschikbaar') \
            and ('woning' not in status.lower()):
            continue

        href = offer.find('a', class_='a').attrs['href']
        city = offer.find('div', class_='objectgegevens').next_element.split('-')[-1].strip()

        price_elem = offer.find(class_='vraagprijs')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((f'https://www.vanderlinden.nl{href}', city, price))
    return urls, True


def parse_vbt(soup):
    urls = []
    for offer in soup.find_all(class_='property svelte-6vswny'):
        status = offer.find(class_=re.compile('status.*svelte-6vswny')).text.strip()
        if status != 'Beschikbaar':
            continue

        city = offer.find(class_='items').div.text

        price_elem = offer.find(class_='price')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((f'https://vbtverhuurmakelaars.nl{offer.attrs["href"]}', city, price))

    navigation_elems = soup.find_all(class_='shiftpage')
    last_page = (len(navigation_elems) == 1) and (navigation_elems[0].text == 'Vorige')
    return urls, last_page


def parse_wooove(soup):
    urls = []
    for offer in soup.find_all(class_='col-xs-12 col-sm-6 col-md-4'):
        
        # filter out garages by price
        # price = offer.find(class_='prijs')
        # price_digits = re.findall(re.compile(r'\d'), price.div.text)
        # price = int(''.join(price_digits)) if price_digits else 0
        # if price < 800:
        #     continue

        status = offer.find(class_=re.compile('statusbutton.*'))
        if status and (status.text.strip() != 'Nieuw!'):
            continue

        href = offer.attrs['href']
        city = offer.find(class_='plaats').text

        price_elem = offer.find(class_='prijs')
        price = re.search(r'[\d.]+', price_elem.text).group().replace('.', '') if price_elem else None

        urls.append((f'https://hurenbijwooove.nl{href}', city, price))
    
    last_page = soup.find(class_='nummers col-xs-12').span.next_sibling is None
    return urls, last_page
