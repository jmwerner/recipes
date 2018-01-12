import sys
sys.path.insert(0, 'generator')

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

def test_degrees_symbol_replacement():
    assert gen.replace_degrees_in_string('110 degrees lit') == '110&#176 lit'
    assert gen.replace_degrees_in_string('110 Degrees lit') == '110&#176 lit'
    assert gen.replace_degrees_in_string('110 degree lit') == '110&#176 lit'
    assert gen.replace_degrees_in_string('110 Degree lit') == '110&#176 lit'
    assert gen.replace_degrees_in_string('110 degreeslit') == '110&#176lit'
    assert gen.replace_degrees_in_string('110 Degreeslit') == '110&#176lit'
    assert gen.replace_degrees_in_string('110 degreelit') == '110&#176lit'
    assert gen.replace_degrees_in_string('110 Degreelit') == '110&#176lit'
    assert gen.replace_degrees_in_string('110degrees lit') == '110degrees lit'
    assert gen.replace_degrees_in_string('110Degrees lit') == '110Degrees lit'
    assert gen.replace_degrees_in_string('110degree lit') == '110degree lit'
    assert gen.replace_degrees_in_string('110Degree lit') == '110Degree lit'
    assert gen.replace_degrees_in_string('110degreeslit') == '110degreeslit'
    assert gen.replace_degrees_in_string('110Degreeslit') == '110Degreeslit'
    assert gen.replace_degrees_in_string('110degreelit') == '110degreelit'
    assert gen.replace_degrees_in_string('110Degreelit') == '110Degreelit'