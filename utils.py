from string import digits, ascii_letters
import random
import datetime
from collections import Counter

RULE_ID = 1

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


def add_auxiliary_columns(data):
    """Add 3 auxiliary columns: Order, Rule Order, Rule Rows which help parse the rules
    Args:
        data (List[list]): Data from excel file
    Returns:
        List[list], which contains info about each rules.
    """

    unique_rules = Counter([row[RULE_ID] for row in data[1:]])
    rule_item = data[1][RULE_ID]
    counter_rule = 1
    new_data = []
    for counter, rule in enumerate(data[1:], start=1):
        rule_id, *other = rule
        if rule_item == rule_id:
            new_data.append([counter, counter_rule, unique_rules[rule_id], rule_id, *other])
            counter_rule += 1
        else:
            counter_rule = 1
            new_data.append([counter, counter_rule, unique_rules[rule_id], rule_id, *other])
            counter_rule += 1
            rule_item = rule[RULE_ID]
    return new_data
