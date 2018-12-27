import pytest
import requests
import urllib.request
import bs4 as bs
import json

from selenium import webdriver

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options  

import sys
sys.path.insert(0, 'generator')
import webpageGenerator as gen

def get_html_from_url(url):
    url_open = urllib.request.urlopen(url)
    raw_page = url_open.read()
    page = raw_page.decode("utf8")
    url_open.close()
    return page

def make_ingredient_dict_from_html(html):
    soup = bs.BeautifulSoup(html, 'lxml')
    ingredient_names_from_html = soup.find_all('span', \
        {'id': lambda L: L and L.startswith('recipeIngredient')})
    ingredient_numbers_from_html = soup.find_all('span', \
        {'id': lambda L: L and L.startswith('recipeNumber')})
    ingredient_units_from_html = soup.find_all('span', \
        {'id': lambda L: L and L.startswith('recipeUnit')})
    ingredient_dict = {}
    if ingredient_names_from_html:
        for i in range(0, len(ingredient_names_from_html)):
            ingredient_id = ingredient_names_from_html[i].get('id')
            ingredient_id = ingredient_id.replace('recipeIngredient-', '')
            ingredient_dict[ingredient_id] = \
                {'name': ingredient_names_from_html[i].text.strip(' \n'), \
                'number': ingredient_numbers_from_html[i].text.strip(' \n'), \
                'units': ingredient_units_from_html[i].text.strip(' \n'), \
                'value_tag':ingredient_numbers_from_html[i].get('value')}
    return ingredient_dict

def create_category_iterator(ingredients_dict):
    unique_categories = ['']
    for i in range(0, len(ingredients_dict)):
        if 'category' in ingredients_dict[i]:
            if ingredients_dict[i]['category'][0] not in unique_categories:
                unique_categories.append(ingredients_dict[i]['category'][0])
    if(len(unique_categories) == 1 and not unique_categories[0]):
        unique_categories = ['noCategory']
    output_dict = {}
    for key in unique_categories:
        output_dict[key] = 0
    return output_dict

def find_ingredient_category(input):
    if 'category' not in input:
        return 'noCategory'
    else:
        if not input['category'][0]:
            return 'noCategory'
        else:
            return input['category'][0]

def process_json_name(input_string):
    output_string = input_string.strip(' \n').lower().title()
    output_string = gen.lower_special_cases_in_string(output_string)
    output_string = gen.replace_degrees_in_string(output_string)
    return output_string

def process_html_ingredient_name(input_string):
    output_string = input_string.replace('°', '&#176')
    return output_string

def process_json_number(input_number):
    return gen.convert_to_mixed_number(input_number)

def process_json_units(input_list, scaling_number = '1'):
    scaling_number_fraction = convert_mixed_number_to_fraction(scaling_number)
    plural = (gen.string_to_float(input_list['number'][0]) * \
              scaling_number_fraction[0] / scaling_number_fraction[1]) > 1.0
    processed_units = gen.set_plural_suffix(input_list['units'][0], plural)
    return processed_units

def process_and_scale_json_number(input_number, scaling_number):
    mixed_number = gen.convert_to_mixed_number(input_number)
    input_number_fraction = convert_mixed_number_to_fraction(mixed_number)
    scaling_number_fraction = convert_mixed_number_to_fraction(scaling_number)
    scaled_fraction = (input_number_fraction[0] * scaling_number_fraction[0], \
                       input_number_fraction[1] * scaling_number_fraction[1])
    scaled_fraction = simplify_fraction(scaled_fraction[0], scaled_fraction[1])
    return gen.convert_to_mixed_number(scaled_fraction)

def convert_mixed_number_to_fraction(input_string):
    splits = input_string.split(' ')
    splits = [x for x in splits if x]
    if len(splits) == 1:
        inner_splits = splits[0].split('/')
        inner_splits = [x for x in inner_splits if x]
        if len(inner_splits) == 1:
            return (int(inner_splits[0]), 1)
        else:
            return (int(inner_splits[0]), int(inner_splits[1]))
    else:
        processed_touple = convert_mixed_number_to_fraction(splits[1])
        output_numerator = \
            processed_touple[0] + int(splits[0]) * processed_touple[1]
        return (output_numerator, processed_touple[1])

def simplify_fraction(numer, denom):
    common_divisor = gcd(numer, denom)
    (reduced_num, reduced_den) = \
        (numer / common_divisor, denom / common_divisor)
    if reduced_den == 1:
        return (int(reduced_num), int(reduced_den))
    elif common_divisor == 1:
        return (numer, denom)
    else:
        return (int(reduced_num), int(reduced_den))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


#########
# Tests #
#########

def test_scaling_helper_functions():
    assert convert_mixed_number_to_fraction('1') == (1,1)
    assert convert_mixed_number_to_fraction('1 ') == (1,1)
    assert convert_mixed_number_to_fraction(' 1') == (1,1)
    assert convert_mixed_number_to_fraction('2/3') == (2,3)
    assert convert_mixed_number_to_fraction(' 2/3') == (2,3)
    assert convert_mixed_number_to_fraction(' 2/3 ') == (2,3)
    assert convert_mixed_number_to_fraction('4 2/3') == (14,3)
    assert convert_mixed_number_to_fraction('5/3') == (5,3)
    assert simplify_fraction(2,3) == (2,3)
    assert simplify_fraction(2,4) == (1,2)
    assert simplify_fraction(5,1) == (5,1)
    assert simplify_fraction(6,3) == (2,1)


# processed_links_from_sitemap = processed_links_from_sitemap(raw_sitemap(sitemap_name()), xml_tag())

def test_recipe_scaling(processed_links_from_sitemap):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    for link in processed_links_from_sitemap:
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(link)
        source_html = browser.page_source
        ingredient_dict_from_html = make_ingredient_dict_from_html(source_html)



# old_browser = webdriver.PhantomJS()
# old_browser.get(link)
# source_html = old_browser.page_source
# ingredient_dict_from_html_2 = make_ingredient_dict_from_html(source_html)

        if ingredient_dict_from_html:

            scaling_vector = browser.execute_script('return scalingValues')
            assert scaling_vector[0] == '1'

            json_link = link.replace('.html', '.json').replace('website/', '')
            json_string = get_html_from_url(json_link)
            ingredients_from_json = \
                json.loads(json.loads(json_string)['ingredients'][0])

            category_iterator = create_category_iterator(ingredients_from_json)

            for i in range(0, len(ingredient_dict_from_html)):
                category = find_ingredient_category(ingredients_from_json[i])
                id = category + '-' + str(category_iterator[category])
                category_iterator[category] += 1

                processed_json_number = \
                    process_json_number(ingredients_from_json[i]['number'][0])
                processed_units = process_json_units(ingredients_from_json[i])

                assert processed_json_number == \
                    ingredient_dict_from_html[id]['number']
                assert process_json_name(ingredients_from_json[i]['name'][0]) \
                    == process_html_ingredient_name(ingredient_dict_from_html[id]['name'])
                assert processed_json_number ==  \
                    ingredient_dict_from_html[id]['value_tag']
                assert processed_units == ingredient_dict_from_html[id]['units']


            # # Open menu (and leave it open)
            # menu_button = browser.find_element_by_id("menu")
            # menu_button.click()

            # for scaling_value in scaling_vector[1:]:

            #     # Click scaling button
            #     scaling_button = browser.find_element_by_id("scalingButton")
            #     scaling_button.click()

            #     # Get html from page after click
            #     source_html = browser.page_source
            #     ingredient_dict_from_html = \
            #         make_ingredient_dict_from_html(source_html)

            #     if ingredient_dict_from_html:

            #         json_link = link.replace('.html', '.json')
            #         json_link = json_link.replace('website/', '')
            #         json_string = get_html_from_url(json_link)
            #         ingredients_from_json = \
            #             json.loads(json.loads(json_string)['ingredients'][0])

            #         category_iterator = \
            #             create_category_iterator(ingredients_from_json)

            #         for i in range(0, len(ingredient_dict_from_html)):
            #             category = \
            #                 find_ingredient_category(ingredients_from_json[i])
            #             id = category + '-' + str(category_iterator[category])
            #             category_iterator[category] += 1

            #             processed_json_number = \
            #                 process_and_scale_json_number(\
            #                 ingredients_from_json[i]['number'][0], \
            #                 scaling_value)
            #             processed_units = \
            #                 process_json_units(ingredients_from_json[i], \
            #                                    scaling_value)

            #             assert processed_json_number == \
            #                 ingredient_dict_from_html[id]['number']
            #             assert process_json_name(\
            #                 ingredients_from_json[i]['name'][0]) == \
            #             ingredient_dict_from_html[id]['name']
            #             assert processed_json_number ==  \
            #                 ingredient_dict_from_html[id]['value_tag']
            #             assert processed_units == \
            #                 ingredient_dict_from_html[id]['units']
