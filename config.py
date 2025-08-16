import parse_funcs


DATA_DIR = 'data'
NEW_OFFERS_FILE = f'{DATA_DIR}/new_offers.txt'
ERRORS_FILE = 'errors.log'
WEBDRIVER = 'geckodriver'

USER_AGENT_VALUE = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'

CORPS = {
    'mvgm': {
        'url': 'https://ikwilhuren.nu/aanbod/?page={page}',
        'parse_func': parse_funcs.parse_mvgm
    },
    # 'vesteda': {
    #     'url': 'https://www.vesteda.com/nl/woning-zoeken?placeType=0&sortType=0&radius=20&s=&sc=woning&latitude=0&longitude=0&filters=0&priceFrom=1000&priceTo=2000',
    #     'parse_func': parse_funcs.parse_vesteda,
    #     'webdriver_params': {
    #         'xpath': '//li[@class="o-layout__cell u-margin-bottom"]',
    #         'timeout': 15
    #     }
    # },
    # 'rebo': {
    #     'url': 'https://rebowonenhuur.nl/zoekopdracht',
    #     'parse_func': parse_funcs.parse_rebo,
    #     'webdriver_params': {
    #         'xpath': '//div[@class="col-12 col-sm-6 col-lg-4 d-flex"]',
    #         'timeout': 15,
    #         'pre-hook-func': parse_funcs.login_rebo
    #     }
    # },
    # 'bouwinvest': {
    #     'url': 'https://www.wonenbijbouwinvest.nl/huuraanbod?price=900-1700&propertyToggle=false&page={page}',
    #     'parse_func': parse_funcs.parse_bouwinvest,
    #     'webdriver_params': {
    #         'xpath': [
    #             '//div[@class="projectproperty-tile box-shadow"]',
    #             '//div[@class="pagination d-flex justify-content-between align-items-center"]'
    #         ],
    #         'timeout': 15
    #     }
    # },
    # 'schep': {
    #     'url': 'https://zoeken.schepvastgoedmanagers.nl/Woning/Pagina/{page}',
    #     'parse_func': parse_funcs.parse_schep
    # },
    # 'stienstra': {
    #     'url': 'https://www.stienstra.nl/uitgebreid-zoeken/page/{page}/?status=te-huur&min-area=0&max-area=600&min-price=0&max-price=500000&sortby=d_date',
    #     'parse_func': parse_funcs.parse_stienstra
    # },
    # 'vanderlinden': {
    #     'url': 'https://www.vanderlinden.nl/woning-huren',
    #     'parse_func': parse_funcs.parse_vanderlinden
    # },
    # 'vbt': {
    #     'url': 'https://vbtverhuurmakelaars.nl/woningen/{page}',
    #     'parse_func': parse_funcs.parse_vbt,
    #     'webdriver_params': {
    #         'pre-hook-func': parse_funcs.accept_cookies_vbt
    #     },
    #     'enforce_static': True
    # },
    # 'wooove': {
    #     'url': 'https://hurenbijwooove.nl/Woning/Pagina/{page}',
    #     'parse_func': parse_funcs.parse_wooove
    # }
}

IGNORED_CITIES = (
    "Amsterdam",
    "Groningen",
    # "Zwolle",
    "Enschede",
    # "Apeldoorn",
    "Arnhem",
    # "Dordrecht",
    "Nijmegen",
    # "'s-Hertogenbosch",
    # "Breda",
    # "Tilburg",
    # "Eindhoven",
    "Maastricht",
    "Assen",
    # "Alkmaar",
    # "Purmerend",
    "Zutphen",
    "Roermond",
    # "Helmond"
)

PRICE_RANGE = (1100, 1700)
