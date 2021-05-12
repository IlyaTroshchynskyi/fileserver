import os
import utils
import openpyxl


def read_file(path_to_file):
    """Read files on your server
    Args:
        path_to_file (srt): Path to file
    Returns:
        content (str): Return content of the file
    """
    try:
        with open(path_to_file, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File wasn't found")


def create_file(length_name, extension, content, letter, digit):
    """Create files on your server with certain extension. If file have existed the
    will raise FileExistsError
    Args:
        length_name (srt): Define length of the file
        extension (str): Define the extension of of the file
        letter (bool): Define do it use the letters in the name of the file
        digit (bool): Define do it use the digits in the name of the file
    """
    try:
        file_name = utils.generate_file_name(length_name=length_name,
                                             letter=letter,
                                             digit=digit,
                                             extension=extension)
        with open(file_name, 'x') as file:
            file.write(content)
            print(f'File was created with name {file_name}')
            return
    except FileNotFoundError:
        print("File wasn't created")


def delete_file(path_to_file):
    """Delete files from your server
    Args:
        path_to_file (srt): Path to file
    """
    try:
        os.remove(path_to_file)
        print("File was deleted successfully")
    except FileNotFoundError:
        print("File wasn't found")


def get_metadata_file(path_to_file):
    """Get meta data about your file.
    Args:
        path_to_file (srt): Path to file
    Returns:
        dict, which contains info about each file. Keys:
                user_id (str): user id
                size_file (int): file size in kilobytes
                last_access (datetime): datetime of last access to the file;
                modification_time (datetime): datetime of last file modification;
                creation_time (datetime): datetime of the creating file;
    """
    try:
        data = os.stat(path_to_file)
        return {'user_id': data.st_dev,
                'size_file': data.st_size,
                'last_access': utils.conversion_date_time(data.st_atime),
                'modification_time': utils.conversion_date_time(data.st_mtime),
                'creation_time': utils.conversion_date_time(data.st_ctime)}
    except FileNotFoundError:
        print("File wasn't found")


def read_excel_file(path_to_file):
    """Read excel file with extension .xlsx from the active sheet.
        Args:
            path_to_file (srt): Path to file
        Returns:
            data (list): Contains all rows of the active sheet of the excel file
        """
    try:
        wb = openpyxl.load_workbook(path_to_file)
    except FileNotFoundError:
        print("File not found")

    worksheet = wb.active
    data = []

    for row in range(1, worksheet.max_row + 1):
        collect_line = []
        for column in range(1, worksheet.max_column + 1):
            collect_line.append(str(worksheet.cell(row=row, column=column).value))
            if column == worksheet.max_column:
                data.append(collect_line)

    return data


d = read_excel_file('InputOutputValidation.xlsx')






