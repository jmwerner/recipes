# import pytest
# import requests
# import urllib.request
# import bs4 as bs
# import json

# import sys
# sys.path.insert(0, 'website_generator')
# import webpageGenerator as gen

# # def get_html_from_url(url):
# #     url_open = urllib.request.urlopen(url)
# #     raw_page = url_open.read()
# #     page = raw_page.decode("utf8")
# #     url_open.close()
# #     return page

# # def make_ingredient_dict_from_link(link):
# #     html = get_html_from_url(link)
# #     soup = bs.BeautifulSoup(html, 'lxml')
# #     ingredient_names_from_html = soup.find_all('span', {'id': lambda L: L and L.startswith('recipeIngredient')})
# #     ingredient_numbers_from_html = soup.find_all('span', {'id': lambda L: L and L.startswith('recipeNumber')})
# #     ingredient_units_from_html = soup.find_all('span', {'id': lambda L: L and L.startswith('recipeUnit')})
# #     ingredient_dict = {}
# #     if len(ingredient_names_from_html) > 0:
# #         for i in range(0, len(ingredient_names_from_html)):
# #             ingredient_id = ingredient_names_from_html[i].get('id').replace('recipeIngredient-', '')
# #             ingredient_dict[ingredient_id] = {'name': ingredient_names_from_html[i].text.strip(' \n'), 'number': ingredient_numbers_from_html[i].text.strip(' \n'), 'units': ingredient_units_from_html[i].text.strip(' \n'), 'value_tag':ingredient_numbers_from_html[i].get('value')}
# #     return ingredient_dict

# # def create_category_iterator(ingredients_dict):
# #     unique_categories = ['']
# #     for i in range(0, len(ingredients_dict)):
# #         if 'category' in ingredients_dict[i]:
# #             if ingredients_dict[i]['category'][0] not in unique_categories:
# #                 unique_categories.append(ingredients_dict[i]['category'][0])
# #     if(len(unique_categories) == 1 and unique_categories[0] == ''):
# #         unique_categories = ['noCategory']
# #     output_dict = {}
# #     for key in unique_categories:
# #         output_dict[key] = 0
# #     return output_dict

# # def find_ingredient_category(input):
# #     if 'category' not in input:
# #         return 'noCategory'
# #     else:
# #         if input['category'][0] == '':
# #             return 'noCategory'
# #         else:
# #             return input['category'][0]

# # def process_json_name(input_string):
# #     output_string = input_string.strip(' \n').lower().title()
# #     output_string = gen.lower_conjunctions_in_ingredients(output_string)
# #     return output_string

# # def process_json_number(input_number):
# #     return gen.convert_to_mixed_number(input_number)

# # def process_json_units(input_list):
# #     plural = gen.string_to_float(input_list['number'][0]) > 1.0
# #     processed_units = gen.set_plural_suffix(input_list['units'][0], plural)
# #     return processed_units

# #########
# # Tests #
# #########



# with Browser() as browser:
#     # Visit URL
#     url = "http://www.google.com"
#     browser.visit(url)
#     browser.fill('q', 'splinter - python acceptance testing for web applications')
#     # Find and click the 'search' button
#     button = browser.find_by_name('btnG')
#     # Interact with elements
#     button.click()
#     if browser.is_text_present('splinter.readthedocs.io'):
#         print("Yes, the official website was found!")
#     else:
#         print("No, it wasn't found... We need to improve our SEO techniques")



# from selenium import webdriver
# browser = webdriver.Chrome()

# browser.get('https://jmwerner.github.io/recipes/website/allRecipes/Appetizer/ArtichokeDip.html')


# menuButton = browser.find_element_by_id("menuButton")
# menuButton.click()

# scalingButton = browser.find_element_by_id("scalingButton")
# scalingButton.click()

# # Functionalize this, as it needs to be called several times
# ingredient_numbers = browser.find_elements_by_class_name('recipeNumber')

# [ingredient_numbers[i].text for i in range(0,len(ingredient_numbers))]





# def test_recipe_scaling(processed_links_from_sitemap):
#     for link in processed_links_from_sitemap:

#         driver = webdriver.Firefox()
#         driver.get(link)

#         ingredient_dict_from_html = make_ingredient_dict_from_link(link)
#         if len(ingredient_dict_from_html) > 0:
        
#             json_link = link.replace('.html', '.json').replace('website/', '')
#             json_string = get_html_from_url(json_link)
#             ingredients_from_json = json.loads(json.loads(json_string)['ingredients'][0])

#             category_iterator = create_category_iterator(ingredients_from_json)

#             for i in range(0, len(ingredient_dict_from_html)):
#                 category = find_ingredient_category(ingredients_from_json[i])
#                 id = category + '-' + str(category_iterator[category])
#                 category_iterator[category] += 1

#                 processed_json_number = process_json_number(ingredients_from_json[i]['number'][0])
#                 processed_units = process_json_units(ingredients_from_json[i])

#                 assert processed_json_number == ingredient_dict_from_html[id]['number']
#                 assert process_json_name(ingredients_from_json[i]['name'][0]) == ingredient_dict_from_html[id]['name']
#                 assert processed_json_number ==  ingredient_dict_from_html[id]['value_tag']
#                 assert processed_units == ingredient_dict_from_html[id]['units']




