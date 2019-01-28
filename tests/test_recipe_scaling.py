import pytest
import bs4 as bs
import json

from selenium import webdriver

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options  


#########
# Tests #
#########

def test_scaling_helper_functions(helpers):
    assert helpers.convert_mixed_number_to_fraction('1') == (1, 1)
    assert helpers.convert_mixed_number_to_fraction('1 ') == (1, 1)
    assert helpers.convert_mixed_number_to_fraction(' 1') == (1, 1)
    assert helpers.convert_mixed_number_to_fraction('2/3') == (2, 3)
    assert helpers.convert_mixed_number_to_fraction(' 2/3') == (2, 3)
    assert helpers.convert_mixed_number_to_fraction(' 2/3 ') == (2, 3)
    assert helpers.convert_mixed_number_to_fraction('4 2/3') == (14, 3)
    assert helpers.convert_mixed_number_to_fraction('1 1/3') == (4, 3)
    assert helpers.convert_mixed_number_to_fraction(' 1 1/3') == (4, 3)
    assert helpers.convert_mixed_number_to_fraction('1 1/3  ') == (4, 3)
    assert helpers.convert_mixed_number_to_fraction('1 1/1') == (2, 1)
    assert helpers.convert_mixed_number_to_fraction('  1  1/1   ') == (2, 1)
    assert helpers.convert_mixed_number_to_fraction('5/3') == (5, 3)
    assert helpers.simplify_fraction(2, 3) == (2, 3)
    assert helpers.simplify_fraction(2, 4) == (1, 2)
    assert helpers.simplify_fraction(5, 1) == (5, 1)
    assert helpers.simplify_fraction(6, 3) == (2, 1)
    assert helpers.simplify_fraction(24, 8) == (3, 1)
    assert helpers.simplify_fraction(32, 24) == (4, 3)
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction('1 2 5/3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction('1 2 5/3 2')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction('1 2 3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction('1/2 2/3 5/3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction('1/2/4 2/2/3 5/3')
    with pytest.raises(Exception) as e_info:
        helpers.convert_mixed_number_to_fraction('')


def test_recipe_page_creation_and_scaling(processed_links_from_sitemap, helpers, root_directory):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    for link in processed_links_from_sitemap:
        local_link = helpers.get_local_file_from_url(link, root_directory)
        ingredient_dict_from_html = helpers.make_ingredient_dict_from_link(helpers, root_directory, local_link)

        browser.get('file://' + local_link)
        source_html = browser.page_source

        # If this is an actual recipe page (and not a category page)
        if ingredient_dict_from_html:

            scaling_vector = browser.execute_script('return scalingValues')
            assert scaling_vector[0] == '1'

            json_link = local_link.replace('.html', '.json').replace('website/', '')
            json_string = helpers.get_html_from_local_file(json_link)
            ingredients_from_json = json.loads(json.loads(json_string)['ingredients'][0])

            category_iterator = helpers.create_category_iterator(ingredients_from_json)

            for i in range(0, len(ingredient_dict_from_html)):
                category = helpers.find_ingredient_category(ingredients_from_json[i])
                id = category + '-' + str(category_iterator[category])
                category_iterator[category] += 1

                processed_json_number = \
                    helpers.process_json_number(ingredients_from_json[i]['number'][0])
                processed_units = helpers.process_json_units(helpers, ingredients_from_json[i])

# Test that the base html matches what is in the json file that created it
                assert processed_json_number == ingredient_dict_from_html[id]['number']
                assert helpers.process_json_name(ingredients_from_json[i]['name'][0]) == helpers.process_html_ingredient_name(ingredient_dict_from_html[id]['name'])
                assert processed_json_number ==  ingredient_dict_from_html[id]['value_tag']
                assert processed_units == ingredient_dict_from_html[id]['units']

# Press the scaling button and test that it changed the html appropriately

            # # Open menu (and leave it open)
            menu_button = browser.find_element_by_id("menuButton")
            menu_button.click()

            for scaling_value in scaling_vector[1:]:

                # Click scaling button
                scaling_button = browser.find_element_by_id("scalingButton")
                scaling_button.click()

                # Get html from page after click
                source_html = browser.page_source
                ingredient_dict_from_html = helpers.make_ingredient_dict_from_html(source_html)

                if ingredient_dict_from_html:

                    json_link = local_link.replace('.html', '.json').replace('website/', '')
                    json_string = helpers.get_html_from_local_file(json_link)
                    ingredients_from_json = json.loads(json.loads(json_string)['ingredients'][0])

                    category_iterator = \
                        helpers.create_category_iterator(ingredients_from_json)

                    for i in range(0, len(ingredient_dict_from_html)):
                        category = helpers.find_ingredient_category(ingredients_from_json[i])
                        id = category + '-' + str(category_iterator[category])
                        category_iterator[category] += 1

                        processed_json_number = \
                            helpers.process_and_scale_json_number(helpers,\
                            ingredients_from_json[i]['number'][0], \
                            scaling_value)
                        processed_units = helpers.process_json_units(helpers, ingredients_from_json[i], scaling_value)

                        assert processed_json_number == ingredient_dict_from_html[id]['number']
                        assert helpers.process_json_name(ingredients_from_json[i]['name'][0]) == helpers.process_html_ingredient_name(ingredient_dict_from_html[id]['name'])
                        assert processed_units == ingredient_dict_from_html[id]['units']
