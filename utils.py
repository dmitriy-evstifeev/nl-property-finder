import os

from requests import post

from config import ERRORS_FILE


def dump_data(loc, data, rec_sep='\n', append=True):
    if not os.path.exists(os.path.dirname(loc)):
        os.makedirs(os.path.dirname(loc))
        
    data_ = [data] if isinstance(data, str) else data
    with open(loc, 'a' if append else 'w') as file:
        for record in data_:
            file.write(f'{record}{rec_sep}')


def load_data(loc):
    data = []
    if os.path.exists(loc):
        with open(loc, 'r') as file:
            for record in file:
                data.append(record.rstrip())
    return data


def log_error(msg):
    dump_data(get_abs_path(ERRORS_FILE), msg)


def get_abs_path(path):
    if os.path.isabs(path):
        return path
    return f'{os.path.dirname(__file__) }/{path}'


def delete_files(*paths):
    for path_ in paths:
        abs_path = get_abs_path(path_)
        try:
            os.remove(abs_path)
        except FileNotFoundError:
            pass


def send_tg_message(msg, token, chat_id, md=True):
    api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': msg,
        'disable_web_page_preview': True,
        'parse_mode': 'HTML'
    }
    post(url=api_url, json=payload)


def compose_offers_message(offers, errors):
    offers = load_data(offers)
    errors = load_data(errors)

    offers_msg = '<b>New offers:</b>\n{}'.format('\n\n'.join(offers)) if offers else ''
    errors_msg = '<b>Exceptions:</b>\n{}'.format('\n'.join(errors)) if errors else ''
    sep = '\n' * 3 if offers and errors else ''

    return f'{offers_msg}{sep}{errors_msg}'
