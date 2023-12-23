import csv
import json
import os
import pathlib
from datetime import date

import constants as const


def init_user_dat(file_path=None):
    if file_path is None:
        file_path = os.path.join(const.DIR_DATA, const.FILE_JSON_USER)

    user_dat = {
        'goal': const.USER_SAVE_GOAL,
        'aim': const.USER_AIM_BUDGET,
        'save': const.USER_SAVE_PERCENTAGE
    }
    with open(file_path, 'w') as json_file:
        json.dump(user_dat, json_file, indent=4)


def init_directories():
    if not check_dir(const.DIR_DATA):
        os.makedirs(const.DIR_DATA)


def parse_date(input_date):
    if isinstance(input_date, date):
        date_parts = [input_date.year, input_date.month, input_date.day]
    else:
        date_parts = [int(input_date[0:4]), int(input_date[5:7]), int(input_date[8:10])]

    return date_parts


def check_dir(dir_path):
    return os.path.exists(dir_path)


def check_file(file_path):
    return pathlib.Path(file_path).is_file()


def check_this_month(input_date):
    parsed_input = parse_date(input_date)
    parsed_today = parse_date(get_today())

    if parsed_input[0] != parsed_today[0]:      # Check year
        return False
    if parsed_input[1] != parsed_today[1]:      # Check month
        return False

    return True


def get_today():
    return date.today()


def get_colors(main_value, check_value, percent=1, reverse=False):
    if not 0 <= percent <= 1:
        print('[ERROR] get_colors()')
        return const.COLOR_GOOD

    if reverse:
        if (main_value * percent) > check_value:
            return const.COLOR_DANGER
        else:
            return const.COLOR_GOOD

    if (main_value * percent) < check_value:
        return const.COLOR_DANGER
    else:
        return const.COLOR_GOOD


def format_2f(input_number):
    return '{:,.2f}'.format(input_number)


def format_to_float(input_string):
    return float(input_string.replace('$', ''))


def format_length(input_string):
    if len(input_string) < const.CONFIG_MAX_LENGTH:
        pad_amount = const.CONFIG_MAX_LENGTH - len(input_string)
        format_string = input_string + const.CONFIG_PAD_CHAR * pad_amount
    else:
        format_string = input_string[:const.CONFIG_MAX_LENGTH][:-3]
        format_string = format_string + '...'

    return format_string


def format_listbox_view(track_item, track_cost, track_date=None):
    if track_date is None:
        track_date = get_today()

    return f'{track_date} | {format_length(track_item)} | ${format_2f(track_cost)}'


def load_user_dat(file_path=None):
    if file_path is None:
        file_path = os.path.join(const.DIR_DATA, const.FILE_JSON_USER)
    if not check_file(file_path):
        init_user_dat(file_path)

    with open(file_path, 'r') as json_file:
        dat_dict = json.load(json_file)

    return dat_dict


def load_tracker(file_path=None):
    if file_path is None:
        file_path = os.path.join(const.DIR_DATA, const.FILE_CSV_TRACKER)
    if not check_file(file_path):
        return []

    dat_list = []
    with open(file_path, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for each_row in csv_reader:
            dat_list.append(each_row)

    return dat_list


def save_tracker(item_name, item_cost, file_path=None):
    if file_path is None:
        file_path = os.path.join(const.DIR_DATA, const.FILE_CSV_TRACKER)

    dat_list = [get_today(), item_name, item_cost]
    with open(file_path, 'a+', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(dat_list)
        print(dat_list)


def update_user_data(dict_key, dict_val, file_path=None):
    if file_path is None:
        file_path = os.path.join(const.DIR_DATA, const.FILE_JSON_USER)

    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)

    json_data[dict_key] = dict_val

    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
