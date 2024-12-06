from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests

from config import DATA_DIR, NEW_OFFERS_FILE, USER_AGENT_VALUE
import utils


class ScrapeException(AttributeError):
    pass


class HouseSeekerBase(ABC):
    _ignored_cities = None

    def __init__(self, name, url, parse_func):
        self.name = name
        self.url = url
        self.parse_func = parse_func

    @classmethod
    def set_ignore_list(cls, ignore_list):
        cls._ignored_cities = ignore_list

    def _get_offers(self):
        offers = []
        page = 1
        current_url = self.url.format(page=page) if '{page}' in self.url else self.url

        while True:
            # print(current_url)
            last_page_signal = True  # in order not to repeat in each exc below
            try:
                page_offers, last_page_signal = self._scrape_page(current_url)
                filtered_offers = self._filter_offers(page_offers)
            except requests.RequestException:
                utils.log_error(f'{self.name}: Request error')
            except ScrapeException:
                utils.log_error(f'{self.name}: Scrapping error')
            except WebDriverException:
                utils.log_error(f'{self.name}: Selenium error')
            else:
                offers.extend(filtered_offers)

            if last_page_signal:
                break
            
            ## DEBUG AREA ###
            # if page > 5: break
            #################
            page += 1
            current_url = self.url.format(page=page)
        return offers
    
    @abstractmethod
    def _scrape_page(self, url_):
        pass

    def _filter_offers(self, raw_offers_):
        if not self._ignored_cities:
            return raw_offers_
        return (o[0] for o in raw_offers_ if o[1] not in self._ignored_cities)

    def _extract_new_offers(self, cur_offers, prev_offers):
        return set(cur_offers) - set(prev_offers)

    def process(self):
        print(f'Processing {self.name}...', end='', flush=True)
        offers_ = self._get_offers()
        if not offers_:
            return
        
        data_path = utils.get_abs_path(f'{DATA_DIR}/{self.name}.txt')
        prev_offers_ = utils.load_data(data_path)
        new_offers = self._extract_new_offers(offers_, prev_offers_)

        if new_offers:
            print(f'{len(new_offers)} new offer(s).', end='')
            utils.dump_data(utils.get_abs_path(NEW_OFFERS_FILE), new_offers)
        utils.dump_data(utils.get_abs_path(data_path), offers_, append=False)
        print()


class HouseSeekerStatic(HouseSeekerBase):
    def _scrape_page(self, url_):
        headers_ = {
            'User-Agent': USER_AGENT_VALUE
        }

        response = requests.get(url=url_, headers=headers_)
        if not response:
            raise requests.RequestException
        return self._parse_html(response.content)
    
    def _parse_html(self, html_content):
        soup_ = BeautifulSoup(html_content, 'html.parser')
        try:
            page_offers_, last_page_ = self.parse_func(soup_)
        except Exception:
            raise ScrapeException
        return page_offers_, last_page_
        

class HouseSeekerDynamic(HouseSeekerStatic):
    def __init__(self, name, url, parse_func, web_driver, web_driver_params):
        super().__init__(name, url, parse_func)
        self.web_driver = web_driver
        self.web_driver_params = web_driver_params
        if self.web_driver_params.get('pre-hook-func'):
            self.web_driver_params['pre-hook-func'](self.web_driver)

    def _scrape_page(self, url_):
        self.web_driver.get(url_)

        if isinstance(self.web_driver_params['xpath'], str):
            xpaths = [self.web_driver_params['xpath']]
        else:
            xpaths = self.web_driver_params['xpath']
        for xpath in xpaths:
            WebDriverWait(self.web_driver, self.web_driver_params.get('timeout', 10)) \
                .until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        return super()._parse_html(self.web_driver.page_source)
