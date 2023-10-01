import parse_funcs


DATA_DIR = 'data'

NEW_OFFERS_FILE = f'{DATA_DIR}/new_offers.txt'
# RENTED_OUT_FILE = 'rented_out.txt'
ERROR_FILE = 'errors.log'

CORPORATIONS = {
    'mvgm': {
        'url': 'https://ikwilhuren.nu/pagina/{PAGE}?',
        'params': {
            'action': 'epl_search',
            'post_type': 'rental',
            'property_price_to': 1750,
            'property_bedrooms_min': 2,
            'sortby': 'status_asc'
        },
        'parse_function': parse_funcs.mvgm_parse 
    },
    'vesteda': {
        'url': 'https://www.vesteda.com/en/unit-search?',
        'params': {
            'placeType': 0,
            'sortType': 0,  # Available first
            'sc': 'woning',
            'filters': '6873,6883,6889',
            'priceFrom': 500,
            'priceTo': 1500
        },
        'parse_function': parse_funcs.vesteda_parse
    },
    'rebo': {
        'url': 'https://www.rebohuurwoning.nl/nl/aanbod',
        'params': {},
        'parse_function': parse_funcs.rebo_parse
    },
    'bouwinvest': {
        'url': 'https://www.wonenbijbouwinvest.nl/huuraanbod?page={PAGE}&',
        'params': {
            'price': '900-1500',
            'surface': '60-130',
            'order': 'recent',
            'propertyToggle': False
        },
        'parse_function': parse_funcs.bouwinvest_parse
    },
    'schep': {
        'url': 'https://schepvastgoedmanagers.nl/Woning/Pagina/{PAGE}',
        'params': {},
        'parse_function': parse_funcs.schep_parse
    }
}