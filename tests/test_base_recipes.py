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

#########
# Tests #
#########

def test_base_recipe_creation(processed_links_from_sitemap):
    for link in processed_links_from_sitemap:
        html = get_html_from_url(link)
        soup = bs.BeautifulSoup(html, 'lxml')
        ingredients_from_html = soup.find_all('span', {'class':'recipeNumber'})

        if len(ingredients_from_html) > 0:
        
            json_link = link.replace('.html', '.json').replace('website/', '')
            json_string = get_html_from_url(json_link)
            ingredients_from_json = json.loads(json.loads(json_string)['ingredients'][0])

            for i in range(0, len(ingredients_from_html)):
                assert ingredients_from_html[i].text.strip(' \n') == convert_to_mixed_number(ingredients_from_json[i]['number'][0])







