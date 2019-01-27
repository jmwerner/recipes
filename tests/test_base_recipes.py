'''Testing script for basic recipe conversion from json'''

import json
import pytest

#########
# Tests #
#########

def test_base_recipe_creation(root_directory, processed_links_from_sitemap, helpers):
    for link in processed_links_from_sitemap:
        ingredient_dict_from_html = helpers.make_ingredient_dict_from_link(helpers, root_directory, link)
        if ingredient_dict_from_html:

            json_link = link.replace('.html', '.json').replace('website/', '')
            local_json_file = helpers.get_local_file_from_url(json_link, root_directory)
            json_string = helpers.get_html_from_local_file(local_json_file)
            ingredients_from_json = \
                json.loads(json.loads(json_string)['ingredients'][0])

            category_iterator = helpers.create_category_iterator(ingredients_from_json)

            for i in range(0, len(ingredient_dict_from_html)):
                category = helpers.find_ingredient_category(ingredients_from_json[i])
                id = category + '-' + str(category_iterator[category])
                category_iterator[category] += 1

                processed_json_number = \
                    helpers.process_json_number(ingredients_from_json[i]['number'][0])
                processed_units = helpers.process_json_units(ingredients_from_json[i])

                assert processed_json_number == \
                    ingredient_dict_from_html[id]['number']
                assert helpers.process_json_name(ingredients_from_json[i]['name'][0]) \
                    == ingredient_dict_from_html[id]['name']
                assert processed_json_number == \
                    ingredient_dict_from_html[id]['value_tag']
                assert processed_units == ingredient_dict_from_html[id]['units']
