import json
import ast
import subprocess
import re

category_tag = '<RECIPE_CATEGORY_GOES_HERE>'
name_tag = '<RECIPE_NAME_GOES_HERE>'
notes_tag = '<RECIPE_NOTES_GO_HERE>'
directions_tag = '<RECIPE_DIRECTIONS_GO_HERE>'
ingredients_tag = '<RECIPE_INGREDIENTS_GO_HERE>'
category_links_tag = '<RECIPE_CATEGORY_LINKS_GO_HERE>'
recipe_links_tag = '<RECIPE_LINKS_GO_HERE>'
menu_links_tag = '<MENU_LINKS_GO_HERE>'


recipe_html_template_path = 'templates/recipeTemplate.html'
category_html_template_path = 'templates/categoryTemplate.html'


def create_ingredients_html(ingredients):
    ingredients_list = ast.literal_eval(ingredients[0])
    if recipe_categories_exist(ingredients_list):
        output_html_string = ''
        ingredient_categories = find_recipe_categories(ingredients_list)
        for ingredient_category in ingredient_categories:
            output_html_string += '<h6>' + ingredient_category + '</h6>'
            category_ingredients = get_ingredients_in_category(ingredients_list, ingredient_category)
            output_html_string += create_html_list_from_ingredients(category_ingredients)
    else:
        output_html_string = create_html_list_from_ingredients(ingredients_list)
    return output_html_string

def get_ingredients_in_category(ingredients_list, ingredient_category):
    output_list = list()
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['category'][0] == ingredient_category:
            output_list.append(ingredients_list[i])
    return output_list

def create_html_list_from_ingredients(ingredients_list):
    output_html_string = '<ul>' + '\n'
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['name'][0] != '':
            output_html_string += '<li>' + ingredients_list[i]['number'][0] + \
                ' ' + ingredients_list[i]['units'][0] + ' ' + \
                ingredients_list[i]['name'][0] +  '</li>' + '\n'
    output_html_string += '</ul>' + '\n'
    return output_html_string

def recipe_categories_exist(ingredients_list):
    category_exists = True
    if 'category' not in list(ingredients_list[0].keys()):
        category_exists = False
    else:
        for i in range(0, len(ingredients_list)):
            if ingredients_list[i]['category'] == ['']:
                category_exists = False
    return category_exists

def find_recipe_categories(ingredients_list):
    all_categories = []
    for i in range(0, len(ingredients_list)):
        all_categories.append(ingredients_list[i]['category'][0])
    unique_categories = list(set(all_categories))
    return unique_categories

def create_directions_html(directions):
    output_html_string = '<ol>' + '\n'
    directions_list = ast.literal_eval(directions[0])
    for i in range(0, len(directions_list)):
        if directions_list[i][0] != '':
            output_html_string += '<li>' + directions_list[i][0] + '</li>' + '\n'
    output_html_string += '</ol>' + '\n'
    return output_html_string

def create_category_menu_links(categories, is_recipe = False):
    if is_recipe:
        extra_path = '../'
    else:
        extra_path = ''

    output_html_string = '<ul>\n'
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

def export_html(path, html_input):
    with open(path, 'w') as html_output_file:
        html_output_file.write(html_input)
    html_output_file.close()

def add_spaces_to_proper(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1)

################################################################################
# Create recipes pages & category pages
################################################################################

all_categories = subprocess.check_output(['ls', '../allRecipes']).decode("utf-8").split('\n')
all_categories = [x for x in all_categories if x]

for recipe_category in all_categories:
    all_recipes_in_category = subprocess.check_output(['ls', '../allRecipes/' + recipe_category]).decode("utf-8").split('\n')
    all_recipes_in_category = [x for x in all_recipes_in_category if x]

    category_html = import_html(category_html_template_path)

    recipes_in_category_html = create_recipes_in_category_link_html(recipe_category, all_recipes_in_category)

    category_menu_links_html = create_category_menu_links(all_categories, is_recipe = False)


    category_html = category_html.replace(category_tag, recipe_category)
    category_html = category_html.replace(recipe_links_tag, recipes_in_category_html)
    category_html = category_html.replace(menu_links_tag, category_menu_links_html)

    export_html('../website/allRecipes/' + recipe_category + '.html', category_html)

    for recipe_in_category in all_recipes_in_category:      
        recipePath = '../allRecipes/' + recipe_category + '/' + recipe_in_category 

        recipe = import_json(recipePath)
        recipe_html = import_html(recipe_html_template_path)

        recipe_name = recipe['recipeName'][0].split('.')[0]

        output_recipe_html_path = '../website/allRecipes/' + remove_spaces(recipe['recipeCategory'][0]) + \
            '/' + remove_spaces(recipe_name) + '.html'


        ingredients_html = create_ingredients_html(recipe['ingredients'])

        directions_html = create_directions_html(recipe['directions'])

        notes_html = create_notes_html(recipe['notes'][0])

        recipe_menu_links_html = create_category_menu_links(all_categories, is_recipe = True)

        recipe_html = recipe_html.replace(category_tag, recipe['recipeCategory'][0])
        recipe_html = recipe_html.replace(name_tag, recipe['recipeName'][0])
        recipe_html = recipe_html.replace(notes_tag, notes_html)
        recipe_html = recipe_html.replace(directions_tag, directions_html)
        recipe_html = recipe_html.replace(ingredients_tag, ingredients_html)
        recipe_html = recipe_html.replace(menu_links_tag, recipe_menu_links_html)

        subprocess.call(["mkdir", "-p", "../website/allRecipes/" + remove_spaces(recipe['recipeCategory'][0])])

        export_html(output_recipe_html_path, recipe_html)

