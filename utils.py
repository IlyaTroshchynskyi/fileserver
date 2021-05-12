from string import digits, ascii_letters
import random
import datetime


def define_symbols_for_name(letter=False, digit=False):
    """ Define what kind of symbols can be in the name of file
    Args:
        letter (bool, optional): Define do it use the letters in the name of the file. Defaults to False.
        digit (bool, optional): Define do it use the digits in the name of the file. Defaults to False.
    Returns:
        possible symbols (str): Possible symbols for name of the file
    """
    possible_symbols = ''
    if letter and digit:
        possible_symbols = ascii_letters + digits
    elif letter:
        possible_symbols = ascii_letters
    elif digit:
        possible_symbols = digits
    return possible_symbols


def generate_file_name(length_name, extension, letter, digit):
    """Generate name of the file based on letters, digits, length and extensions
    Args:
        length_name (srt): Define length of the file
        extension (str): Define the extension of of the file
        letter (bool): Define do it use the letters in the name of the file
        digit (bool): Define do it use the digits in the name of the file
    Returns:
        file_name (str)
    """

    possible_symbols = define_symbols_for_name(letter, digit)
    return ''.join(random.choices(list(possible_symbols), k=length_name)) + extension


def conversion_date_time(data):
    """Convert date in certain format. Time comes in seconds from 01.01.1970 year
    Args:
        data (date)
    Returns:
        DateTime (datetime):  in format %Y-%m-%d %H:%M:%S
    """
    return datetime.datetime.fromtimestamp(data).strftime('%Y-%m-%d %H:%M:%S')