import re


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

        city_elem = offer.find(class_='card-body d-flex flex-column').find('span')
        city = ' '.join(city_elem.text.split()[1:]) if city_elem else 'Unknown'
        
        urls.append((f'https://ikwilhuren.nu{href}', city))
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

        urls.append((f'https://www.vesteda.com{href}', city))
    return urls, True


def parse_rebo(soup):
    urls = []
    for offer in soup.find_all(class_='property js-object-item'):
        label_elem = offer.find(class_='label')
        label = label_elem.text.lower() if label_elem else ''
        if label == 'garage':
            continue
        if label == 'complex':
            break

        href = offer.find('a').attrs.get('href')
        if href:
            try:
                city = offer.find(class_='text').find('h4').text
            except Exception:  # too generic...
                city = 'Unknown'
            urls.append((f'https://www.rebohuurwoning.nl{href}', city))
    return urls, True


# With status checking: doesn't work correctly without Selenium. Dynamically ipdates statuses
# ===========
# def parse_bouwinvest(soup):
#     urls = []
#     offers = soup.find_all(class_='projectproperty-tile box-shadow')
#     for offer in offers:
#         status = soup.find(class_='sticker-bar sticker-bar__top').next_element
#         if not 'beschikbaar' in status.lower():
#             continue
#         urls.append(offer['href'])
#     return urls, not bool(len(offers))

def parse_bouwinvest(soup):
    urls = []
    for offer in soup.find_all(class_='projectproperty-tile box-shadow'):
        city = offer.find(class_='paragraph fw-light').text
        urls.append((offer['href'], city))
    return urls, not bool(len(urls))


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
        urls.append((f'https://schepvastgoedmanagers.nl{href}', city))
    else:
        last_page = not len(urls)
    return urls, last_page
