import utils
import file_service
import pytest


@pytest.mark.parametrize("path_to_file", ['InputOutputValidation.xlsx'])
def test_read_excel_file(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)) > 0

