import os
import utils


def read_file(path_to_file):
    try:
        if os.path.isfile(path_to_file):
            with open(path_to_file, 'r') as file:
                content = file.read()
                print(content)
        else:
            print("File wasn't found")
    except FileNotFoundError as e:
           print("File wasn't found")


def create_file(length_name, extension, content, letters, digit):
    try:
        file_name = utils.generate_file_name(length_name=length_name,
                                            letters=letters, digit=digit, extension=extension)
        if not os.path.isfile(file_name):
            with open(file_name, 'w') as file:
                file.write(content)
                print('File was created')
                return
        else:
            print("Such file exist")
    except FileNotFoundError as e:
           print("File wasn't created")


def delete_file(path_to_file):
    try:
        if os.path.isfile(path_to_file):
            os.remove(path_to_file)
            print("File was deleted successfully")
        else:
            print("File wasn't found")
    except FileNotFoundError as e:
           print("File wasn't found")


def get_metadata_file(path_to_file):
    try:
        if os.path.isfile(path_to_file):
            data = os.stat(path_to_file)
            print({'user_id': data.st_dev, 'size_file': data.st_size,
                   'last_access': utils.conversion_date_time(data.st_atime),
                   'modification_time': utils.conversion_date_time(data.st_mtime),
                   'creation_time': utils.conversion_date_time(data.st_ctime)})
        else:
            print("File wasn't found")
    except FileNotFoundError as e:
        print("File wasn't found")