from datetime import datetime
from os import devnull, environ, path
from sys import argv

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from HouseSeeker import HouseSeekerBase, HouseSeekerDynamic, HouseSeekerStatic
import config
import utils


def init_webdriver(file_name):
    service = Service(executable_path=file_name, log_output=devnull)
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    # options.set_preference('permissions.default.stylesheet', 2)
    options.set_preference('permissions.default.image', 2)  # Block images from loading
    return webdriver.Firefox(service=service, options=options)


def process_urls(corps=None):
    utils.delete_files(config.ERRORS_FILE, config.NEW_OFFERS_FILE)
    HouseSeekerBase.set_ignore_list(config.IGNORED_CITIES)
    HouseSeekerBase.set_price_range(*config.PRICE_RANGE)

    webdriver = None

    if corps:
        corps_to_process = {k: v for k, v in config.CORPS.items() if k in corps}
    else:
        corps_to_process = config.CORPS

    for corp, params in corps_to_process.items():
        webdriver_params = params.get('webdriver_params')
        if webdriver_params and not params.get('enforce_static', False):
            webdriver = webdriver or init_webdriver(utils.get_abs_path(config.WEBDRIVER))
            corp = HouseSeekerDynamic(corp, params['url'], params['parse_func'], webdriver, webdriver_params)
        else:
            corp = HouseSeekerStatic(corp, params['url'], params['parse_func'])

        corp.process()

    if webdriver:
        webdriver.quit()


def main():
    print(f'[{datetime.now()}] Starting process...')

    is_init = not path.exists(utils.get_abs_path(config.DATA_DIR))

    load_dotenv()
    bot_token = environ['TG_BOT_TOKEN']
    # chat_id = environ['TG_CHAT_ID']
    chat_id = environ['TG_TEST_CHAT_ID']

    args = argv[1:]
    corps_ = None
    if args and args[0].endswith('corps'):
        corps_ = args[1].split(',')

    try:
        process_urls(corps_)
    except Exception as e:
        ex_msg = f'<b>Unforeseen exception:</b>\n{e}'
        # print(ex_msg)
        utils.send_tg_message(ex_msg, bot_token, chat_id)
        quit()

    message = utils.compose_offers_message(
        offers=utils.get_abs_path(config.NEW_OFFERS_FILE),
        errors=utils.get_abs_path(config.ERRORS_FILE)
    )

    if is_init:
        utils.send_tg_message('Process initialized.', bot_token, chat_id)
    else:
        utils.send_tg_message(message, bot_token, chat_id)

    print('Processing completed.')


if __name__ == '__main__':
    main()
