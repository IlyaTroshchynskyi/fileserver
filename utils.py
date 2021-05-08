from string import digits, ascii_letters
import random
import datetime


def generate_file_name(length_name, extension, letters=False, digit=False):
    possible_symbols = ''
    if letters and digit:
        possible_symbols = ascii_letters + digits
    elif letters:
        possible_symbols = ascii_letters
    elif digit:
        possible_symbols = digits

    return ''.join(random.choices(list(possible_symbols), k=length_name)) + extension



def conversion_date_time(data):
    return datetime.datetime.fromtimestamp(data).strftime('%Y-%m-%d %H:%M:%S')