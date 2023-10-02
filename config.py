import parse_funcs


DATA_DIR = 'data'
NEW_OFFERS_FILE = f'{DATA_DIR}/new_offers.txt'
ERRORS_FILE = 'errors.log'
WEBDRIVER = 'geckodriver'

CORPS = {
    'mvgm': {
        'url': 'https://ikwilhuren.nu/aanbod/?page={page}',
        'parse_func': parse_funcs.parse_mvgm
    },
    'vesteda': {
        'url': 'https://www.vesteda.com/nl/woning-zoeken?placeType=0&sortType=0&radius=20&s=&sc=woning&latitude=0&longitude=0&filters=0&priceFrom=900&priceTo=1500',
        'parse_func': parse_funcs.parse_vesteda,
        'webdriver_params': {
            'xpath': '//li[@class="o-layout__cell u-margin-bottom"]',
            'timeout': 15
        }
    },
    'rebo': {
        'url': 'https://www.rebohuurwoning.nl/nl/aanbod',
        'parse_func': parse_funcs.parse_rebo
    },
    'bouwinvest': {
        'url': 'https://www.wonenbijbouwinvest.nl/huuraanbod?price=900-1700&propertyToggle=false&page={page}',
        'parse_func': parse_funcs.parse_bouwinvest
    },
    'schep': {
        'url': 'https://schepvastgoedmanagers.nl/Woning/Pagina/{page}',
        'parse_func': parse_funcs.parse_schep
    }
}

IGNORED_CITIES = (
    "Groningen",
    "Zwolle",
    "Enschede",
    "Apeldoorn",
    "Arnhem",
    "Dordrecht",
    "Nijmegen",
    "'s-Hertogenbosch",
    "Breda",
    "Tilburg",
    "Eindhoven",
    "Maastricht"
)
