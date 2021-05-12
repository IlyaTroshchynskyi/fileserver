import utils
import file_service
import pytest
import re


def test_read_file():
    data = 'some text'
    assert file_service.read_file('test1.txt') == data


@pytest.mark.parametrize("path_to_file", ['InputOutputValidation.xlsx'])
def test_read_excel_file(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)) > 0


@pytest.mark.parametrize("path_to_file", ['InputOutputValidation.xlsx'])
def test_read_excel_file_all_rows(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)) == 13


@pytest.mark.parametrize("path_to_file", ['InputOutputValidation.xlsx'])
def test_read_excel_file_all_columns(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)[0]) == 9


def test_symbols_for_name():
    name = utils.define_symbols_for_name(True, True)
    assert True if re.search('[^A-za-z0-9]', name) else False == False


def test_zero_length_file_name():
    assert len(utils.generate_file_name(5, '.py', True, True)) == 8


@pytest.mark.parametrize("extension", ['.py', '.txt, .xml', '.css', '.html'])
def test_extension_file(extension):
    assert utils.generate_file_name(5, extension, True, True).endswith(extension)