'''This script generates the recipes website and all subpages'''

import json
import ast
import subprocess
import re
from bs4 import BeautifulSoup

CATEGORY_TAG = '<RECIPE_CATEGORY_GOES_HERE>'
NAME_TAG = '<RECIPE_NAME_GOES_HERE>'
NOTES_TAG = '<RECIPE_NOTES_GO_HERE>'
WINE_PAIRING_TAG = '<RECIPE_WINE_PAIRING_GOES_HERE>'
DIRECTIONS_TAG = '<RECIPE_DIRECTIONS_GO_HERE>'
INGREDIENTS_TAG = '<RECIPE_INGREDIENTS_GO_HERE>'
RECIPE_LINKS_TAG = '<RECIPE_LINKS_GO_HERE>'
MENU_LINKS_TAG = '<MENU_LINKS_GO_HERE>'
RECIPE_ORIGIN_TAG = '<RECIPE_ORIGIN_GOES_HERE>'
RECIPE_GLASS_TYPE_TAG = '<RECIPE_GLASS_TYPE_GOES_HERE>'

RECIPE_HTML_TEMPLATE_PATH = 'templates/recipeTemplate.html'
CATEGORY_HTML_TEMPLATE_PATH = 'templates/categoryTemplate.html'


def create_ingredients_html(ingredients, name_of_recipe):
    '''Creates html of recipe ingredients and category headings for webpage.
    Args:
        ingredients (list of dicts): Ingredient name, number, and units dicts
            that come from the recipe json.
        name_of_recipe (string): Name of recipe to which the ingredients
            list corresponds.
    Returns:
        string: html string to be added to webpage.
    '''
    ingredients_list = ast.literal_eval(ingredients[0])
    ingredients_list = preprocess_ingredients(ingredients_list)
    if recipe_categories_exist(ingredients_list, name_of_recipe):
        output_html_string = ''
        ingredient_categories = find_recipe_categories(ingredients_list)
        for ingredient_category in ingredient_categories:
            output_html_string += '<h6>' + ingredient_category + '</h6>'
            category_ingredients = \
                get_ingredients_in_category(ingredients_list, \
                                            ingredient_category)
            output_html_string += \
                create_cat_ingred_html(category_ingredients, \
                                       ingredient_category)
    else:
        output_html_string = \
            create_cat_ingred_html(ingredients_list, 'noCategory')
    return output_html_string

def preprocess_ingredients(ingredients_list):
    '''Preprocess list of recipe ingredients.
    Args:
        ingredients_list (list): List of ingredient dicts coming from raw
            recipe json.
    Returns:
        list: Processed list of ingredient dicts.
    '''
    output_list = ingredients_list
    for i in range(0, len(output_list)):
        if output_list[i]['number'][0] != '':
            plural = string_to_float(output_list[i]['number'][0]) > 1.0
            output_list[i]['units'][0] = \
                set_plural_suffix(output_list[i]['units'][0], plural)
            output_list[i]['name'][0] = \
                output_list[i]['name'][0].lower().title()
            output_list[i]['name'][0] = \
                lower_special_cases_in_string(output_list[i]['name'][0])
            output_list[i]['name'][0] = \
                replace_degrees_in_string(output_list[i]['name'][0])
    return output_list

def lower_special_cases_in_string(ingredient):
    '''Converts special cases to non-capitalized words in recipe ingredients.
    Args:
        ingredient (string): Ingredient name string for processing.
    Returns:
        string: Processed ingredient name string with special cases lowered.
    '''
    conjunctions = ['For', 'And', 'Nor', 'But', 'Or', 'Yet', 'So', 'Per', 'Of']
    splits = ingredient.strip().split()
    for i in range(0, len(splits)):
        if splits[i] in conjunctions:
            splits[i] = splits[i].lower()
        splits[i] = splits[i].replace("'S", "'s")
    return ' '.join(splits)

def replace_degrees_in_string(ingredient):
    '''Replaces variants of the word degree with the degrees symbol.
    Args:
        ingredient (string): Ingredient name string for processing.
    Returns:
        string: Processed ingredient name string with degrees symbols.
    '''
    ingredient = ingredient.replace(' Degrees', '&#176')
    ingredient = ingredient.replace(' degrees', '&#176')
    ingredient = ingredient.replace(' Degree', '&#176')
    ingredient = ingredient.replace(' degree', '&#176')
    return ingredient

def set_plural_suffix(input_string, plural):
    '''Changes plural suffix on words where applicable and strips (s) option.
    Args:
        input_string (string): Recipe units string.
        plural (bool): Logical to convert input_string to plural or not.
    Returns:
        string: Recipe units with appropriate plural or non-plural ending.
    '''
    # Also removing trailing s from mistake in early version of input app
    base_string = input_string.replace('s(s)', '')
    base_string = base_string.replace('(s)', '')
    base_string = base_string.replace('(es)', '')
    if plural and base_string != 'Whole':
        if base_string == 'Dash' or base_string == 'Pinch':
            output = base_string + 'es'
        else:
            output = base_string + 's'
    else:
        output = base_string
    return output

def string_to_float(input_string):
    '''Converts a string of numbers or a fraction to a float.
    Args:
        input_string (string): String of numbers or a fraction for conversion.
    Returns:
        float: Number post conversion of input_string.
    '''
    splits = input_string.split('/')
    if len(splits) == 1:
        output = float(input_string)
    else:
        output = float(splits[0]) / float(splits[1])
    return output

def get_ingredients_in_category(ingredients_list, ingredient_category):
    '''Finds all recipe ingredients in specified category.
    Args:
        ingredients_list (list): List of ingredient dicts.
        ingredient_category (string): Name of desired ingredient_category.
    Returns:
        list: Ingredient dicts that correspond to ingredient_category.
    '''
    output_list = list()
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['category'][0] == ingredient_category:
            output_list.append(ingredients_list[i])
    return output_list

def create_cat_ingred_html(ingredients_list, ingredient_category):
    '''Creates html of ingredients from category for webpage.
    Args:
        ingredients_list (list): List of ingredient dicts.
        ingredient_category (string): Name of desired ingredient_category.
    Returns:
        string: html of category ingredients for webpage.
    '''
    output_html_string = '<ul>' + '\n'
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['name'][0] != '':
            ingredient_number = \
                convert_to_mixed_number(ingredients_list[i]['number'][0])
            output_html_string += \
                '<li><span class=\"recipeNumber\" id=\"recipeNumber-' + \
                str(ingredient_category) + '-' + str(i) + '\" value=\"' + \
                ingredient_number + '\">' + ingredient_number + '</span>' + \
                ' ' + '<span id=\"recipeUnit-' + str(ingredient_category) + \
                '-' + str(i) + '\">' + ingredients_list[i]['units'][0] + \
                '</span> ' + '<span id=\"recipeIngredient-' + \
                str(ingredient_category) + '-' + str(i) + '\">' + \
                ingredients_list[i]['name'][0] + '</span></li>' + '\n'
    output_html_string += '</ul>' + '\n'
    return output_html_string

def convert_to_mixed_number(input_string):
    '''Converts a string of integers or a fraction to a mixed number.
    Args:
        input_string (string): String to be converted to a mixed number.
    Returns:
        string: Mixed number output.
    '''
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

def recipe_categories_exist(ingredients_list, name_of_recipe):
    '''Checks to see if recipe categories exist and makes sure all categories
       are either filled in or all are empty.
    Args:
        ingredients_list (list): List of ingredients from recipe json.
        name_of_recipe (string): Name of current recipe.
    Returns:
        bool: Indicator of category existence.
    '''
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
                    name_of_recipe)
            else:
                categories_exist = False
        else:
            categories_exist = True
    return categories_exist

def find_recipe_categories(ingredients_list):
    '''Find all categories for given recipe.
    Args:
        ingredients_list (list): List of ingredients from recipe json.
    Returns:
        list: All categories.
    '''
    unique_categories = []
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['category'][0] not in unique_categories:
            unique_categories.append(ingredients_list[i]['category'][0])
    return unique_categories

def create_directions_html(directions):
    '''Create html of recipe directions.
    Args:
        directions (list): All directions from recipe json.
    Returns:
        string: html of directions to be included in webpage.
    '''
    directions_list = ast.literal_eval(directions[0])
    directions_list = preprocess_directions(directions_list)
    output_html_string = '<ol>' + '\n'
    for i in range(0, len(directions_list)):
        if directions_list[i][0] != '':
            output_html_string += '<li>' + directions_list[i][0] + '</li>\n'
    output_html_string += '</ol>' + '\n'
    return output_html_string

def create_glass_type_html(recipe):
    '''Create html of glass type for cocktails.
    Args:
        recipe (list): Entire recipe json.
    Returns:
        string: html of glass type to be included in webpage, if applicable.
    '''
    if 'glassType' in recipe:
        if recipe['glassType'][0] == '':
            output_html_string = ''
        else:
            output_html_string = 'output string goes here'
    else:
        output_html_string = ''
    return output_html_string

def create_recipe_origin_html(recipe_source):
    '''Create html of recipe origin person.
    Args:
        recipe_source (string): Origin of recipe.
    Returns:
        string: html of recipe origin to be included in webpage.
    '''
    if recipe_source not in ['NA', '']:
        recipe_origin_string = '<p><i> Recipe from '
        recipe_origin_string += recipe_source
        recipe_origin_string += '</i></p>'
    else:
        recipe_origin_string = ''
    return recipe_origin_string


p = re.compile(r'((?<=[\.\?!]\s)(\w+)|(^\w+))')

def cap(match):
    return(match.group().capitalize())



def capitalize_sentences(input):
    '''Capitalize the first word in every sentence of a string.
    Args:
        input (string): A string of one or many sentences.
    Returns:
        string: Properly capitalized string.
    '''
    regex = re.compile(r'((?<=[\.\?!]\s)(\w+)|(^\w+))')
    def capitalize(match):
        return(match.group().capitalize())
    return regex.sub(capitalize, input)

def preprocess_directions(directions):
    '''Preprocesses directions text.
    Args:
        directions (list): All direction strings from the recipe json.
    Returns:
        list: Processed directions.
    '''
    output = directions
    # Add period to end of direction sentence if not there.
    for i in range(0, len(directions)):
        if output[i][0] != '':
            output[i][0] = output[i][0].rstrip().rstrip('.') + '.'
    # Change ' Degrees' or ' degrees' to the degree symbol
    for i in range(0, len(directions)):
        if output[i][0] != '':
            output[i][0] = replace_degrees_in_string(output[i][0])
    # Remove extra period if exclamation point is present
    for i in range(0, len(directions)):
        if output[i][0] != '':
            output[i][0] = output[i][0].replace('!.', '!')
    # Capitalize first letter of every sentence
    for i in range(0, len(directions)):
        if output[i][0] != '':
            output[i][0] = capitalize_sentences(output[i][0])
    return output

def create_menu_links(categories, is_recipe=False):
    '''Creates links, scaling button, and search box for menu where applicable.
    Args:
        categories (list): All recipe categories.
        is_recipe (bool): Indication of whether or not the menu is for a
            recipe webpage or non-recipe webpage (like a category page).
    Returns:
        string: html for page menu.
    '''
    output_html_string = ''

    if is_recipe:
        extra_path = '../'
    else:
        extra_path = ''

    output_html_string += '<button onclick=\"enterKeyRedirect()\" id=\"search'
    output_html_string += 'Button\" style=\"float:right\">Search</button>'
    output_html_string += '<div style=\"overflow:hidden; padding-right:'
    output_html_string += ' .5em;\"><input class=\"searchField\" '
    output_html_string += 'id=\"searchTxt\" maxlength=\"512\" name=\"search'
    output_html_string += 'Txt\" placeholder=\"Search Here...\" type=\"text\" '
    output_html_string += 'style=\"width: 100%\"/>'
    output_html_string += '</div>'
    output_html_string += '<br><br>'
    if is_recipe:
        output_html_string += '<button id=\"scalingButton\" onClick=\"rescale'
        output_html_string += 'Recipe()\">1X</button>'
        output_html_string += '<br><br>'

    output_html_string += '<ul>\n'
    output_html_string += '<li><a href=\"../' + extra_path + 'index.html\">'
    output_html_string += 'Home</a></li>\n'

    for i in range(0, len(categories)):
        output_html_string += '<li><a href=\"' + extra_path + categories[i] + \
            '.html\">' + add_spaces_to_proper(categories[i]) + '</a></li>\n'
    output_html_string += '</ul>'
    return output_html_string

def create_recipes_in_cat_html(category, recipes_in_category):
    '''Create html category page of all recipes in category.
    Args:
        category (string): Name of category.
        recipes_in_category (list): All recipe names in given category.
    Returns:
        string: html of links to recipe pages for category.
    '''
    output_html_string = '<ul class = "actions vertical">\n'
    for i in range(0, len(recipes_in_category)):
        name_of_recipe = recipes_in_category[i].split('.')[0]
        if i % 2 == 0:
            class_name = 'button'
        else:
            class_name = 'button special'
        output_html_string += '<li><a href=\"' + category + '/' + \
            remove_spaces(add_spaces_to_proper(name_of_recipe).title()) + \
            '.html\" class=\"' + class_name + '\"">' + \
            add_spaces_to_proper(name_of_recipe) + '</a></li>\n'
    output_html_string += '</ul>'
    return output_html_string

def create_notes_html(notes):
    '''Creates html of notes from notes component of recipe json.
    Args:
        notes (string): Notes that were input in the recipe 'notes' section.
    Returns:
        string: html of notes to be included in webpage.
    '''
    if not notes:
        output_html_string = ''
    else:
        output_html_string = '<h5>Notes</h5>\n<p>' + notes + '</p>'
    return output_html_string

def create_wine_pairing_html(recipe):
    '''Creates html of wine pairing from recipe json.
    Args:
        recipe (dict): reading of recipe json created by input app.
    Returns:
        string: html of wine pairing to be included in webpage.
    '''
    if 'winePairing' in recipe:
        if recipe['winePairing'][0] == '':
            output_html_string = ''
        else:
            output_html_string = '<h5>Wine Pairing</h5>\n<p>' + recipe['winePairing'][0] + '</p>'
    else:
        output_html_string = ''
    return output_html_string

def create_sitemap(sitemap_urls):
    '''Creates xml sitemap from list of urls.
    Args:
        sitemap_urls (list of strings): All recipe urls for sitemap.
    Returns:
        string: Sitemap of xml format to be submitted to google custom search.
    '''
    output_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
    output_string += \
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        output_string += '<url>\n<loc>'
        output_string += url
        output_string += '</loc>\n</url>'
    output_string += '</urlset>'
    return output_string

def remove_spaces(string):
    '''Removes spaces from string.
    Args:
        string (string): Collection of characters with or without spaces.
    Returns:
        string: Same input string but without spaces.
    '''
    return string.replace(' ', '')

def import_json(path):
    '''Imports json from file.
    Args:
        path (string): Path to json file to be read.
    Returns:
        string: json that was read from file.
    '''
    with open(path, 'r') as recipe_file:
        json_read_recipe = json.load(recipe_file)
    recipe_file.close()
    return json_read_recipe

def import_html(path):
    '''Imports html from file.
    Args:
        path (string): Path to html file to be read.
    Returns:
        string: html that was read from file.
    '''
    with open(path, 'r') as html_file:
        html = html_file.read()
    html_file.close()
    return html

def export_string_to_file(path, html_input, string_format='lxml'):
    '''Writes xml/html string to provided path.
    Args:
        path (string): Path of where to output file, including file name.
        html_input (string): Raw xml/html string that is to be written.
        string_format (string): Format of string to be provided to
            BeautifulSoup parser.
    Returns:
        None
    '''
    output_string = prettify_string(html_input, string_format)
    with open(path, 'w') as output_file:
        output_file.write(output_string)
    output_file.close()

def prettify_string(html_string, string_format):
    '''Converts html string to string with appropriate indenting and spacing.
    Args:
        html_string (string): Raw html string to be converted.
        string_format (string): Format of the incoming string to be passed to
            the BeautifulSoup converter.
    Returns:
        string: Output html with better spacing and tabs for viewing.
    '''
    parsed_html = BeautifulSoup(html_string, string_format)
    html_string = parsed_html.prettify()
    return html_string

def add_spaces_to_proper(name):
    '''Converts a ProperCaseString into a string with spaces.
    Args:
        name (string): String to be converted.
    Returns:
        string: Converted string.
    '''
    return re.sub(r"(?<=\w)([A-Z])", r" \1", name)

def find_all_recipe_categories():
    '''Finds all recipe categories from file system structure.
    Args:
        None
    Returns:
        list: Names of all recipe categories.
    '''
    categories = subprocess.check_output(['ls', '../allRecipes'])
    categories = categories.decode("utf-8").split('\n')
    categories = [x for x in categories if x]
    return categories

################################################################################
# Create recipes pages & category pages
################################################################################

if __name__ == '__main__':

    ALL_CATEGORIES = find_all_recipe_categories()
    ALL_URLS = []

    for recipe_category in ALL_CATEGORIES:
        all_recipes_in_category = subprocess.check_output(\
            ['ls', '../allRecipes/' + recipe_category])
        all_recipes_in_category = all_recipes_in_category.decode("utf-8")
        all_recipes_in_category = all_recipes_in_category.split('\n')
        all_recipes_in_category = [x for x in all_recipes_in_category if x]

        category_html = import_html(CATEGORY_HTML_TEMPLATE_PATH)

        recipes_in_category_html = \
            create_recipes_in_cat_html(recipe_category, \
                                       all_recipes_in_category)

        category_menu_links_html = create_menu_links(ALL_CATEGORIES, \
                                                     is_recipe=False)

        category_html = category_html.replace(CATEGORY_TAG, \
            add_spaces_to_proper(recipe_category))
        category_html = category_html.replace(RECIPE_LINKS_TAG, \
                                              recipes_in_category_html)
        category_html = category_html.replace(MENU_LINKS_TAG, \
                                              category_menu_links_html)

        category_page_name = '/website/allRecipes/' + recipe_category + '.html'
        ALL_URLS.append('http://jmwerner.github.io/recipes' + \
                        category_page_name)
        export_string_to_file('..' + category_page_name, category_html)

        for recipe_in_category in all_recipes_in_category:
            current_recipe_path = '../allRecipes/' + recipe_category + '/' + \
                recipe_in_category

            recipe = import_json(current_recipe_path)
            recipe_html = import_html(RECIPE_HTML_TEMPLATE_PATH)

            recipe_name = recipe['recipeName'][0].split('.')[0]

            output_recipe_html_path = '/website/allRecipes/' + \
                remove_spaces(recipe['recipeCategory'][0]) + \
                '/' + remove_spaces(recipe_name.title()) + '.html'
            ALL_URLS.append('http://jmwerner.github.io/recipes' + \
                            output_recipe_html_path)

            ingredients_html = create_ingredients_html(recipe['ingredients'], \
                                                       recipe_in_category)
            directions_html = create_directions_html(recipe['directions'])
            glass_type_html = create_glass_type_html(recipe)
            notes_html = create_notes_html(recipe['notes'][0])
            wine_pairing_html = create_wine_pairing_html(recipe)
            recipe_menu_links_html = create_menu_links(ALL_CATEGORIES, \
                                                       is_recipe=True)
            recipe_origin_html = \
                create_recipe_origin_html(recipe['recipeSource'][0])

            recipe_html = recipe_html.replace(CATEGORY_TAG, \
                                              recipe['recipeCategory'][0])
            recipe_html = recipe_html.replace(NAME_TAG, \
                                              recipe['recipeName'][0])
            recipe_html = recipe_html.replace(NOTES_TAG, notes_html)
            recipe_html = recipe_html.replace(WINE_PAIRING_TAG, \
                                              wine_pairing_html)
            recipe_html = recipe_html.replace(DIRECTIONS_TAG, directions_html)
            recipe_html = recipe_html.replace(RECIPE_GLASS_TYPE_TAG, \
                                              glass_type_html)
            recipe_html = recipe_html.replace(INGREDIENTS_TAG, \
                                              ingredients_html)
            recipe_html = recipe_html.replace(MENU_LINKS_TAG, \
                                              recipe_menu_links_html)
            recipe_html = recipe_html.replace(RECIPE_ORIGIN_TAG, \
                                              recipe_origin_html)

            subprocess.call(["mkdir", "-p", "../website/allRecipes/" + \
                            remove_spaces(recipe['recipeCategory'][0])])

            export_string_to_file('..' + output_recipe_html_path, recipe_html)


    SITEMAP_STRING = create_sitemap(ALL_URLS)
    export_string_to_file('../sitemap.xml', SITEMAP_STRING, "xml")
