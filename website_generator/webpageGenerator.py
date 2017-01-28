import json
import ast
import subprocess
import re
from bs4 import BeautifulSoup

category_tag = '<RECIPE_CATEGORY_GOES_HERE>'
name_tag = '<RECIPE_NAME_GOES_HERE>'
notes_tag = '<RECIPE_NOTES_GO_HERE>'
directions_tag = '<RECIPE_DIRECTIONS_GO_HERE>'
ingredients_tag = '<RECIPE_INGREDIENTS_GO_HERE>'
category_links_tag = '<RECIPE_CATEGORY_LINKS_GO_HERE>'
recipe_links_tag = '<RECIPE_LINKS_GO_HERE>'
menu_links_tag = '<MENU_LINKS_GO_HERE>'
recipe_origin_tag = '<RECIPE_ORIGIN_GOES_HERE>'

recipe_html_template_path = 'templates/recipeTemplate.html'
category_html_template_path = 'templates/categoryTemplate.html'


def create_ingredients_html(ingredients, recipe_name):
    ingredients_list = ast.literal_eval(ingredients[0])
    ingredients_list = preprocess_ingredients(ingredients_list)
    if recipe_categories_exist(ingredients_list, recipe_name):
        output_html_string = ''
        ingredient_categories = find_recipe_categories(ingredients_list)
        for ingredient_category in ingredient_categories:
            output_html_string += '<h6>' + ingredient_category + '</h6>'
            category_ingredients = get_ingredients_in_category(ingredients_list, ingredient_category)
            output_html_string += create_html_list_from_ingredients(category_ingredients, ingredient_category)
    else:
        output_html_string = create_html_list_from_ingredients(ingredients_list, 'noCategory')
    return output_html_string

def preprocess_ingredients(ingredients_list):
    output_list = ingredients_list
    for i in range(0, len(output_list)):
        if output_list[i]['number'][0] != '':
            plural = string_to_float(output_list[i]['number'][0]) > 1.0
            output_list[i]['units'][0] = set_plural_suffix(output_list[i]['units'][0], plural)
            output_list[i]['name'][0] = output_list[i]['name'][0].lower().title()
            output_list[i]['name'][0] = lower_conjunctions_in_ingredients(output_list[i]['name'][0])
    return output_list

def lower_conjunctions_in_ingredients(ingredient):
    conjunctions = ['For', 'And', 'Nor', 'But', 'Or', 'Yet', 'So']
    splits = ingredient.strip().split()
    for i in range(0, len(splits)):
        if splits[i] in conjunctions:
            splits[i] = splits[i].lower()
    return ' '.join(splits)

def set_plural_suffix(string, plural):
    # Also removing trailing s from mistake in early version of input app
    base_string = string.replace('s(s)', '')
    base_string = base_string.replace('(s)', '')
    base_string = base_string.replace('(es)', '')
    if plural and base_string != 'Whole' and base_string != 'Pinch':
        if base_string == 'Dash':
            output = base_string + 'es'
        else:
            output = base_string + 's'
    else:
        output = base_string
    return output

def string_to_float(string):
    splits = string.split('/')
    if len(splits) == 1:
        output = float(string)
    else: 
        output = float(splits[0]) / float(splits[1])
    return output

def get_ingredients_in_category(ingredients_list, ingredient_category):
    output_list = list()
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['category'][0] == ingredient_category:
            output_list.append(ingredients_list[i])
    return output_list

def create_html_list_from_ingredients(ingredients_list, ingredient_category):
    output_html_string = '<ul>' + '\n'
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['name'][0] != '':
            ingredient_number = convert_to_mixed_number(ingredients_list[i]['number'][0])
            output_html_string += '<li><span class=\"recipeNumber\" value=\"' + \
                ingredient_number + '\">' + ingredient_number + '</span>' + \
                ' ' + ingredients_list[i]['units'][0] + ' ' + \
                '<span class=\"recipeIngredient\">' + \
                ingredients_list[i]['name'][0] +  '</span></li>' + '\n'
    output_html_string += '</ul>' + '\n'
    return output_html_string

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

def recipe_categories_exist(ingredients_list, recipe_name):
    if 'category' not in list(ingredients_list[0].keys()):
        # Accomodation for older versions of the recipe input app
        categories_exist = False
    else:
        all_categories = []
        for i in range(0, len(ingredients_list)):
            if ingredients_list[i]['number'] != ['']:
                all_categories.append(ingredients_list[i]['category'][0])
        unique_categories = list(set(all_categories))
        if '' in unique_categories:
            if len(unique_categories) > 1:
                raise ValueError('Not all categories were filled in for ' + \
                    recipe_name)
            else:
                categories_exist = False
        else:
            categories_exist = True
    return categories_exist

def find_recipe_categories(ingredients_list):
    unique_categories = []
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['category'][0] not in unique_categories:
            unique_categories.append(ingredients_list[i]['category'][0])
    return unique_categories

def create_directions_html(directions):
    directions_list = ast.literal_eval(directions[0])
    directions_list = preprocess_directions(directions_list)
    output_html_string = '<ol>' + '\n'
    for i in range(0, len(directions_list)):
        if directions_list[i][0] != '':
            output_html_string += '<li>' + directions_list[i][0] + '</li>' + '\n'
    output_html_string += '</ol>' + '\n'
    return output_html_string

def create_recipe_origin_html(recipe_source):
    if recipe_source not in ['NA', '']:
        recipe_origin_html = '<p><i> Recipe from '
        recipe_origin_html += recipe_source
        recipe_origin_html += '</i></p>'
    else:
        recipe_origin_html = ''
    return recipe_origin_html

def preprocess_directions(directions):
    output = directions
    # Add period to end of direction sentence if not there.
    for i in range(0, len(directions)):
        if output[i][0] != '':
            output[i][0] = output[i][0].rstrip().rstrip('.') + '.'
    return output

def create_menu_links(categories, is_recipe = False):
    output_html_string = ''

    if is_recipe:
        extra_path = '../'
    else:
        extra_path = ''

    output_html_string += '<button onclick=\"enterKeyRedirect()\" id=\"searchButton\" style=\"float:right\">Search</button>'
    output_html_string += '<div style=\"overflow:hidden; padding-right: .5em;\">'
    output_html_string += '<input class=\"searchField\" id=\"searchTxt\" maxlength=\"512\" name=\"searchTxt\" placeholder=\"Search Here...\" type=\"text\" style=\"width: 100%\"/>'
    output_html_string += '</div>'
    output_html_string += '<br><br>'
    output_html_string += '<button id=\"scalingButton\" onClick=\"rescaleRecipe()\">1X</button>'     
    output_html_string += '<br><br>'
    output_html_string += '<ul>\n'
    output_html_string += '<li><a href=\"../' + extra_path + 'index.html\">Home</a></li>\n'

    for i in range(0, len(categories)):
        output_html_string += '<li><a href=\"' + extra_path + categories[i] + '.html\">' + \
            add_spaces_to_proper(categories[i]) + '</a></li>\n'
    output_html_string += '</ul>'
    return output_html_string

def create_recipes_in_category_link_html(category, recipes_in_category):
    output_html_string = '<ul class = "actions vertical">\n'
    for i in range(0, len(recipes_in_category)):
        recipe_name = recipes_in_category[i].split('.')[0]
        if i % 2 == 0:
            class_name = 'button'
        else:
            class_name = 'button special'
        output_html_string += '<li><a href=\"' + category + '/' + recipe_name + \
            '.html\" class=\"' + class_name + '\"">' + add_spaces_to_proper(recipe_name) + '</a></li>\n'
    output_html_string += '</ul>'
    return output_html_string

def create_notes_html(raw_notes):
    if len(raw_notes) == 0:
        output_html_string = ''
    else:
        output_html_string = '<h5>Notes</h5>\n<p>' + raw_notes + '</p>'
    return output_html_string

def create_sitemap(all_urls):
    output_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output_string += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in all_urls: 
        output_string += '<url>\n<loc>'
        output_string += url
        output_string += '</loc>\n</url>'
    output_string += '</urlset>'
    return output_string

def remove_spaces(string):
    return string.replace(' ', '')

def import_json(path):
    with open(path, 'r') as recipe_file:
        recipe = json.load(recipe_file)
    recipe_file.close()
    return recipe

def import_html(path):
    with open(path, 'r') as html_file:
        html = html_file.read()
    html_file.close()
    return html

def export_string_to_file(path, html_input, string_format = "lxml"):
    output_string = prettify_string(html_input, string_format)
    with open(path, 'w') as output_file:
        output_file.write(output_string)
    output_file.close()

def prettify_string(html_string, string_format):
    parsed_html = BeautifulSoup(html_string, string_format)
    html_string = parsed_html.prettify()
    return html_string

def add_spaces_to_proper(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)

################################################################################
# Create recipes pages & category pages
################################################################################

if __name__ == '__main__':

    all_categories = subprocess.check_output(['ls', '../allRecipes']).decode("utf-8").split('\n')
    all_categories = [x for x in all_categories if x]
    all_urls = []

    for recipe_category in all_categories:
        all_recipes_in_category = subprocess.check_output(['ls', '../allRecipes/' + recipe_category]).decode("utf-8").split('\n')
        all_recipes_in_category = [x for x in all_recipes_in_category if x]

        category_html = import_html(category_html_template_path)

        recipes_in_category_html = create_recipes_in_category_link_html(recipe_category, all_recipes_in_category)

        category_menu_links_html = create_menu_links(all_categories, is_recipe = False)

        category_html = category_html.replace(category_tag, add_spaces_to_proper(recipe_category))
        category_html = category_html.replace(recipe_links_tag, recipes_in_category_html)
        category_html = category_html.replace(menu_links_tag, category_menu_links_html)

        category_page_name = '/website/allRecipes/' + recipe_category + '.html'
        all_urls.append('https://jmwerner.github.io/recipes' + category_page_name)
        export_string_to_file('..' + category_page_name, category_html)

        for recipe_in_category in all_recipes_in_category: 
            recipePath = '../allRecipes/' + recipe_category + '/' + recipe_in_category 

            recipe = import_json(recipePath)
            recipe_html = import_html(recipe_html_template_path)

            recipe_name = recipe['recipeName'][0].split('.')[0]

            output_recipe_html_path = '/website/allRecipes/' + remove_spaces(recipe['recipeCategory'][0]) + \
                '/' + remove_spaces(recipe_name) + '.html'
            all_urls.append('https://jmwerner.github.io/recipes' + output_recipe_html_path)

            ingredients_html = create_ingredients_html(recipe['ingredients'], recipe_in_category)
            directions_html = create_directions_html(recipe['directions'])
            notes_html = create_notes_html(recipe['notes'][0])
            recipe_menu_links_html = create_menu_links(all_categories, is_recipe = True)
            recipe_origin_html = create_recipe_origin_html(recipe['recipeSource'][0])

            recipe_html = recipe_html.replace(category_tag, recipe['recipeCategory'][0])
            recipe_html = recipe_html.replace(name_tag, recipe['recipeName'][0])
            recipe_html = recipe_html.replace(notes_tag, notes_html)
            recipe_html = recipe_html.replace(directions_tag, directions_html)
            recipe_html = recipe_html.replace(ingredients_tag, ingredients_html)
            recipe_html = recipe_html.replace(menu_links_tag, recipe_menu_links_html)
            recipe_html = recipe_html.replace(recipe_origin_tag, recipe_origin_html)

            subprocess.call(["mkdir", "-p", "../website/allRecipes/" + remove_spaces(recipe['recipeCategory'][0])])

            export_string_to_file('..' + output_recipe_html_path, recipe_html)


    sitemap_string = create_sitemap(all_urls)
    export_string_to_file('../sitemap.xml', sitemap_string, "xml")


