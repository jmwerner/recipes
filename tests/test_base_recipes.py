import pytest
import requests
import urllib.request
import bs4 as bs
import json

def convert_to_mixed_number(input_string):
    splits = input_string.split('/')
    if len(splits) == 1:
        fraction_parts = float(input_string).as_integer_ratio()
    else: 
        fraction_parts = (int(splits[0]), int(splits[1]))
    leading_integer = fraction_parts[0] // fraction_parts[1]
    fraction_numerator = fraction_parts[0] % fraction_parts[1]
    output_string = ''
    if leading_integer > 0:
        output_string += str(leading_integer)
        if fraction_numerator > 0:
            output_string += ' '
    if fraction_numerator > 0:
        output_string += str(fraction_numerator) + '/' + str(fraction_parts[1])
    return output_string

def get_html_from_url(url):
    url_open = urllib.request.urlopen(url)
    raw_page = url_open.read()
    page = raw_page.decode("utf8")
    url_open.close()
    return page

def make_ingredient_dict_from_link(link):
    html = get_html_from_url(link)
    soup = bs.BeautifulSoup(html, 'lxml')
    ingredient_dict = {}
    ingredient_names_from_html = soup.find_all('span', {'class':'recipeIngredient'})
    ingredient_numbers_from_html = soup.find_all('span', {'class':'recipeNumber'})    
    if len(ingredient_names_from_html) > 0:
        for i in range(0, len(ingredient_names_from_html)):
            name = ingredient_names_from_html[i].text.strip(' \n')
            ingredient_dict[name] = ingredient_numbers_from_html[i].text.strip(' \n')
    return ingredient_dict

def lower_conjunctions_in_ingredients(ingredient):
    conjunctions = ['For', 'And', 'Nor', 'But', 'Or', 'Yet', 'So']
    splits = ingredient.strip().split()
    for i in range(0, len(splits)):
        if splits[i] in conjunctions:
            splits[i] = splits[i].lower()
    return ' '.join(splits)

#########
# Tests #
#########

def test_base_recipe_creation(processed_links_from_sitemap):
    for link in processed_links_from_sitemap:
        ingredient_dict_from_html = make_ingredient_dict_from_link(link)
        print(link)
        if len(ingredient_dict_from_html) > 0:
        
            json_link = link.replace('.html', '.json').replace('website/', '')
            json_string = get_html_from_url(json_link)
            ingredients_from_json = json.loads(json.loads(json_string)['ingredients'][0])

            for i in range(0, len(ingredient_dict_from_html)):
                ingredient_name = ingredients_from_json[i]['name'][0].strip(' \n').lower().title()
                ingredient_name = lower_conjunctions_in_ingredients(ingredient_name)
                ingredient_number = convert_to_mixed_number(ingredients_from_json[i]['number'][0])
                assert ingredient_dict_from_html[ingredient_name] == ingredient_number















