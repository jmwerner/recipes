import sys
sys.path.insert(0, 'website_generator')

import webpageGenerator as gen

# Basic tests for the webpage generator, more will be added if necessary

def test_set_plural_suffix():
    assert gen.set_plural_suffix('hello(s)', True) == 'hellos'
    assert gen.set_plural_suffix('hello(s)', False) == 'hello'
    assert gen.set_plural_suffix('hellos', True) == 'helloss'
    assert gen.set_plural_suffix('hellos', False) == 'hellos'

def test_convert_to_mixed_number():
    assert gen.convert_to_mixed_number('5') == '5'
    assert gen.convert_to_mixed_number('1 ') == '1'
    assert gen.convert_to_mixed_number(' 1 ') == '1'
    assert gen.convert_to_mixed_number('1.5') == '1 1/2'
    assert gen.convert_to_mixed_number('3/2') == '1 1/2'
    assert gen.convert_to_mixed_number(' 3 / 2 ') == '1 1/2'
    assert gen.convert_to_mixed_number('1/2') == '1/2'
    assert gen.convert_to_mixed_number('.5') == '1/2'
    assert gen.convert_to_mixed_number('5/1') == '5'
    assert gen.convert_to_mixed_number('11/3') == '3 2/3'

