import os
from urllib.parse import urlencode

import requests


def compose_url(url, params):
    return f'{url}{urlencode(params)}'


def get_root_dir():
    return os.path.dirname(__file__) 


def get_abs_path(path):
    if not os.path.isabs(path):
        return f'{get_root_dir()}/{path}'
    return path


def add_dir(dir_name):
    path_abs = get_abs_path(dir_name)
    if os.path.exists(path_abs):
        return
    os.mkdir(path_abs)


def dump_data(data, loc, rec_sep='\n', append=False):
    loc_abs = get_abs_path(loc)
    write_method = 'a' if append else 'w'
    # data_ = [data] if isinstance(data, str) else data
    with open(loc_abs, write_method) as file:
        for record in data:
            file.write(f'{record}{rec_sep}')


def load_data(loc):
    data = []
    loc_abs = get_abs_path(loc)
    if not os.path.exists(loc_abs):
        return data
    with open(loc_abs, 'r') as file:
        for record in file:
            data.append(record.rstrip())
    return data


def list_dir_files(dir):
    dir_abs = get_abs_path(dir)

    items = []
    if os.path.isfile(dir_abs):
        return [dir]
    for item in os.listdir(dir_abs):
        items.extend(list_dir_files(f'{dir}/{item}'))
    return items


def format_message(header, body):
    # if not body:
    #     return ''
    sep = '\n-'
    body_formatted = sep.join(body)
    return f'{header}:{sep}{body_formatted}'


def send_tg_message(token, chat_id, msg):
    api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': msg,
        'disable_web_page_preview': True
        # 'parse_mode': 'MarkdownV2'
    }
    requests.post(url=api_url, json=payload)

