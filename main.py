from os import environ

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

import utils
from config import CORPORATIONS, DATA_DIR, ERROR_FILE
from HouseChecker import HouseChecker


def main():
    service = Service(executable_path=f'{utils.get_root_dir()}/geckodriver')
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference('permissions.default.stylesheet', 2)
    options.set_preference('permissions.default.image', 2)  # Block images from loading
    driver = webdriver.Firefox(service=service, options=options)

    HouseChecker.driver = driver

    HouseChecker.prepare_dir()

    is_initial_run = not bool(utils.list_dir_files(DATA_DIR))

    for corp, params in CORPORATIONS.items():
        full_url = utils.compose_url(params['url'], params['params'])
        site = HouseChecker(name=corp, url=full_url, parse_func=params['parse_function'])
        site.process_offers()

    load_dotenv()
    token = environ['TG_BOT_TOKEN']
    chat_id = environ['TG_CHAT_ID']
    
    if is_initial_run:
        if utils.get_abs_path(ERROR_FILE) in utils.list_dir_files(utils.get_root_dir()):
            message = 'Initialized with exceptions.'
        else:
            message = 'Initialized successfully.'
    else:
        message = HouseChecker.compose_message()
    
    # utils.send_tg_message(token, chat_id, message)


if __name__ == '__main__':
    main()
