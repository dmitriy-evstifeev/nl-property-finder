import os

from selenium.common.exceptions import StaleElementReferenceException

import utils
from config import DATA_DIR, NEW_OFFERS_FILE, ERROR_FILE


class HouseChecker:
    driver = None
    _has_exceptions = False
    _has_new_offers = False

    def __init__(self, name,url, parse_func):
        self.url = url
        self.name = name
        self.parse_func = parse_func

    def _get_available_offers(self):
        offers = []
        page = 1
        is_last_page = False
        current_url = self.url.format(PAGE=page) if '{PAGE}' in self.url else self.url

        attempt = 1
        while not is_last_page:
            # print(current_url)
            self.driver.get(current_url)
            try:
                page_offers, last_page_signal = self.parse_func(self.driver)
            except StaleElementReferenceException as e:
                if attempt <= 5:
                    print(f'Attempt #{attempt} has failed.')
                    attempt += 1
                    continue
                raise e

            offers.extend(page_offers)
            attempt = 1

            if last_page_signal:
                is_last_page = True
            else:
                page += 1
                current_url = self.url.format(PAGE=page)
        return offers
    
    def _extract_new_offers(self, cur_offers, prev_offers):
        return set(cur_offers) - set(prev_offers)
    
    # def _extract_lost_offers(self, cur_offers, prev_offers):
    #     return set(prev_offers) - set(cur_offers)
    
    def process_offers(self):
        print(f'Processing {self.name}...', end='', flush=True)
        try:
            offers_ = self._get_available_offers()
        except Exception as e:
            ex_text = str(e).split('\n')[0]
            # ex_text = str(e)
            error_msg = f'{self.name}: {ex_text}\n'
            utils.dump_data(error_msg, ERROR_FILE, rec_sep='', append=True)
            self.__class__._has_exceptions = True
            return
        
        prev_offers_path = f'{DATA_DIR}/{self.name}.txt'
        prev_offers_ = utils.load_data(prev_offers_path)
        new_offers = self._extract_new_offers(offers_, prev_offers_)
        if new_offers:
            utils.dump_data(new_offers, NEW_OFFERS_FILE, append=True)
            self.__class__._has_new_offers = True
            print(f'{len(new_offers)} new offer(s)', end='')
        
        utils.dump_data(offers_, prev_offers_path)
        print()
        
    @staticmethod
    def prepare_dir():
        for file in NEW_OFFERS_FILE, ERROR_FILE:
            if utils.get_abs_path(file) in utils.list_dir_files(utils.get_root_dir()):
                os.remove(utils.get_abs_path(file))
                # print('removed: ', file)
        
        utils.add_dir(DATA_DIR)

    @classmethod
    def compose_message(cls):
        msgs = []
        if cls._has_new_offers:
            offers_data = utils.load_data(utils.get_abs_path(NEW_OFFERS_FILE))
            offers_msg = utils.format_message('New offers', offers_data)
            msgs.append(offers_msg)
        if cls._has_exceptions:
            ex_data = utils.load_data(utils.get_abs_path(ERROR_FILE))
            ex_msg = utils.format_message('Exceptions', ex_data)
            msgs.append(ex_msg)


        return '\n'.join(msgs)

        
