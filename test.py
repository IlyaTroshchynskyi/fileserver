import re
import os
from unittest import mock
import coverage
import http
import json
import pytest
import utils
import file_service
from app import app


rules = [
    ['1', '1', '3', 'rule 1', 'Rule 1: Marker DA + Marker IB = Marker RA', 'LHS', 'mark_da', '700', '+', 'N', '1'],
    ['1', '1', '3', 'rule 1', 'Rule 1: Marker DA + Marker IB = Marker RA', 'LHS', 'mark_da', '700', '+', 'N', '1'],
    ['2', '2', '3', 'rule 1', 'Rule 1: Marker DA + Marker IB = Marker RA', 'LHS', 'mark_ib', '800', '=', 'N', '1'],
    ['3', '3', '3', 'rule 1', 'Rule 1: Marker DA + Marker IB = Marker RA', 'RHS', 'mark_ra', '1000', '', 'N', '1'],
    ['4', '1', '2', 'rule 2', 'Rule 2: A >or= 90% of B', 'LHS', 'a', '100', '>=90%', 'N', '1'],
    ['5', '2', '2', 'rule 2', 'Rule 2: A >or= 90% of B', 'RHS', 'a', '100', '', 'N', '1'],
    ['6', '1', '2', 'rule 3', 'Rule 3: Sum of A and C <= 200 threshold (no RHS)', 'LHS', 'a', '200000', '+', 'Y', '1000'],
    ['7', '2', '2', 'rule 3', 'Rule 3: Sum of A and C <= 200 threshold (no RHS)', 'LHS', 'c', '-100', '=<200', 'Y', '1'],
    ['8', '1', '5', 'rule 4', 'Rule 4: (A1+A2+A3)/days number in 2nd half month = B1', 'LHS', 'A1', '1000', '(+', 'N', '1'],
    ['9', '2', '5', 'rule 4', 'Rule 4: (A1+A2+A3)/days number in 2nd half month = B1', 'LHS', 'A2', '350', '+', 'N', '1'],
    ['10', '3', '5', 'rule 4', 'Rule 4: (A1+A2+A3)/days number in 2nd half month = B1', 'LHS', 'A3', '250', ')/', 'N', '1'],
    ['11', '4', '5', 'rule 4', 'Rule 4: (A1+A2+A3)/days number in 2nd half month = B1', 'LHS', 'days_mth_end', '16', '==', 'N',
     '1'],
    ['12', '5', '5', 'rule 4', 'Rule 4: (A1+A2+A3)/days number in 2nd half month = B1', 'RHS', 'B1', '100', '', 'N', '1'],
]
file_param = {"length_name": 5, "extension": ".txt", "content": "HI REST",  "letter": True, "digit": False}

@pytest.fixture(scope='function')
def temp_file(tmp_path):
    file = tmp_path / "filename.txt"
    file.write_text('Content')
    return file


def test_read_file():
    with open('test_data/test1.txt', 'w') as file:
        file.write('some text')
    data = 'some text'
    assert file_service.read_file('test_data/test1.txt') == data


def test_delete_file(temp_file):
    file_service.delete_file(temp_file)
    assert os.path.exists(temp_file) is False


@pytest.mark.parametrize("path_to_file", [os.path.join(os.getcwd(), 'test_data', 'InputOutputValidation_v2.xlsx')])
def test_read_excel_file(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)) > 0


@pytest.mark.parametrize("path_to_file", [os.path.join(os.getcwd(), 'test_data', 'InputOutputValidation_v2.xlsx')])
def test_read_excel_file_all_rows(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)) == 13


@pytest.mark.parametrize("path_to_file", [os.path.join(os.getcwd(), 'test_data', 'InputOutputValidation_v2.xlsx')])
def test_read_excel_file_all_columns(path_to_file):
    assert len(file_service.read_excel_file(path_to_file)[0]) == 11


def test_symbols_for_name():
    name = utils.define_symbols_for_name(True, True)
    assert not re.search('[^A-za-z0-9]', name)


def test_zero_length_file_name():
    assert len(utils.generate_file_name(5, '.py', True, True)) == 8


@pytest.mark.parametrize("extension", ['.py', '.txt, .xml', '.css', '.html'])
def test_extension_file(extension):
    assert utils.generate_file_name(5, extension, True, True).endswith(extension)


@pytest.mark.parametrize('formulas, expect_result', [('os.remove("somefile.txt")', None),
                                                        ('4+3', 7), ('2+2*2', 6)])
def test_evaluate_amount(formulas, expect_result):
    assert file_service._evaluate_amount(formulas) == expect_result


@pytest.fixture(scope="module")
def add_columns():
    return file_service._add_additional_columns(rules)


def test_cal_result_exist_all_rules(add_columns):
    data = add_columns
    data = file_service._combine_formulas(data)
    data = file_service._calculate_results(data)
    assert data[-1][0] == rules[-1][3]


def test_combine_formulas_contain_all_rules(add_columns):
    data = add_columns
    data = file_service._combine_formulas(data)
    data = set([row[0] for row in data])
    assert len(data.difference(set([rule[3] for rule in rules[1:]]))) == 0


@pytest.mark.parametrize('formulas, expected_results', [('1=1', ['1', '1']),
                                                        ('1==1', ['1', '1']),
                                                        ('1<>1', ['1', '1']),
                                                        ('1!=1', ['1', '1']),
                                                        ('1>=1', ['1', '1']),
                                                        ('1=<1', ['1', '1']),
                                                        ('1>1', ['1', '1']),
                                                        ('1=1',  ['1', '1'])])
def test_split_formula(formulas, expected_results):
    assert file_service._split_formula(formulas) == expected_results


@mock.patch("utils.generate_file_name")
def test_generate_file_name(mock_generate_file_name):
    mock_generate_file_name.return_value = 'file.txt'
    assert utils.generate_file_name(4, '.txt', True, True) == 'file.txt'


@pytest.fixture
def client():

    with app.test_client() as client:
        yield client


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == http.HTTPStatus.OK


def test_create_file(client):
    resp = client.get('/create-file')
    assert resp.status_code == http.HTTPStatus.OK


def test_update_file(client):
    file_name = file_service.create_file(*file_param.values())
    resp = client.get(f'/update/{file_name}')
    assert resp.status_code == http.HTTPStatus.OK


def test_get_meta_data1(client):
    file_name = file_service.create_file(*file_param.values())
    resp = client.get(f'/get-meta-data/{file_name}')
    assert resp.status_code == http.HTTPStatus.OK


def test_parse_rules(client):

    resp = client.get('/parse-rules')
    assert resp.status_code == http.HTTPStatus.OK


def test_upload_file(client):
    resp = client.get('/upload_file')
    assert resp.status_code == http.HTTPStatus.OK


def test_create_file1(client):
    resp = client.get('/create-file')
    assert resp.status_code == http.HTTPStatus.OK


def test_create_file1(client):
    resp = client.post('/files', data=dict(length=5, extension='.txt',
    content='dfd', letter=True, digit=True), follow_redirects=True)
    assert b'was created successfully' not in resp.data


def test_update_file1(client):
    resp = client.put('/files/3jQ.txt', data=dict(content="TEST CONTENT"))
    print(resp)
    assert b'TEST CONTENT' not in resp.data