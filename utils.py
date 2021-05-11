from string import digits, ascii_letters
import random
import datetime


def define_symbols_for_name(letter=False, digit=False):
    possible_symbols = ''
    if letter and digit:
        possible_symbols = ascii_letters + digits
    elif letter:
        possible_symbols = ascii_letters
    elif digit:
        possible_symbols = digits
    return possible_symbols


def generate_file_name(length_name, extension, letter, digit):
    possible_symbols = define_symbols_for_name(letter, digit)
    return ''.join(random.choices(list(possible_symbols), k=length_name)) + extension


def conversion_date_time(data):
    return datetime.datetime.fromtimestamp(data).strftime('%Y-%m-%d %H:%M:%S')