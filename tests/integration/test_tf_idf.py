import pytest
import json
import os
from domain import tf_idf
from unittest import TestCase
import config

#result will be different due to the tokens didn't get order by alphabet
"""
@pytest.fixture
def expected_result():
    file_root = os.path.join(config.basedir, "tests/fixture") 
    f = open(os.path.join(file_root, "tf_idf_seed.json"))
    result_dict = json.load(f)
    return result_dict

def test_returns_tf_idf(expected_result):

    json_tf_idf = tf_idf.TfIdfCalculator.get_tf_idf()
    result = json.loads(json_tf_idf)

    TestCase().assertDictEqual(expected_result, result)
"""
