import pytest
import requests
import urllib.request
import bs4 as bs
import json

from selenium import webdriver

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options  


#########
# Tests #
#########

def test_scaling_helper_functions(helpers):
    assert helpers.convert_mixed_number_to_fraction(helpers, '1') == (1, 1)
    assert helpers.convert_mixed_number_to_fraction(helpers, '1 ') == (1, 1)
    assert helpers.convert_mixed_number_to_fraction(helpers, ' 1') == (1, 1)
    assert helpers.convert_mixed_number_to_fraction(helpers, '2/3') == (2, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, ' 2/3') == (2, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, ' 2/3 ') == (2, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, '4 2/3') == (14, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, '1 1/3') == (4, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, ' 1 1/3') == (4, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, '1 1/3  ') == (4, 3)
    assert helpers.convert_mixed_number_to_fraction(helpers, '1 1/1') == (2, 1)
    assert helpers.convert_mixed_number_to_fraction(helpers, '  1  1/1   ') == (2, 1)
    assert helpers.convert_mixed_number_to_fraction(helpers, '5/3') == (5, 3)
    assert helpers.simplify_fraction(helpers, 2, 3) == (2, 3)
    assert helpers.simplify_fraction(helpers, 2, 4) == (1, 2)
    assert helpers.simplify_fraction(helpers, 5, 1) == (5, 1)
    assert helpers.simplify_fraction(helpers, 6, 3) == (2, 1)
    assert helpers.simplify_fraction(helpers, 24, 8) == (3, 1)
    assert helpers.simplify_fraction(helpers, 32, 24) == (4, 3)
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction(helpers, '1 2 5/3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction(helpers, '1 2 5/3 2')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction(helpers, '1 2 3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction(helpers, '1/2 2/3 5/3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction(helpers, '1/2/4 2/2/3 5/3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction(helpers, '')

        
