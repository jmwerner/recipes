
import json
import ast
import subprocess

category_tag = '<RECIPE_CATEGORY_GOES_HERE>'
name_tag = '<RECIPE_NAME_GOES_HERE>'
notes_tag = '<RECIPE_NOTES_GOES_HERE>'
directions_tag = '<RECIPE_DIRECTIONS_GO_HERE>'
ingredients_tag = '<RECIPE_INGREDIENTS_GO_HERE>'

html_template_path = 'templates/recipeTemplate.html'

def create_ingredients_html(ingredients):
    output_html_string = '<ul>' + '\n'
    ingredients_list = ast.literal_eval(ingredients[0])
    for i in range(0, len(ingredients_list)):
        if(ingredients_list[i]['name'][0] != ''):
            output_html_string = output_html_string + \
                '<li>' + ingredients_list[i]['number'][0] + ' ' + \
                         ingredients_list[i]['units'][0] + ' ' + \
                         ingredients_list[i]['name'][0] +  \
                '</li>' + '\n'
    output_html_string = output_html_string + '</ul>' + '\n'
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

################################################################################

all_categories = subprocess.check_output(['ls', '../allRecipes']).decode("utf-8").split('\n')

for recipe_category in all_categories:
    if recipe_category != '':
        all_recipes_in_category = subprocess.check_output(['ls', '../allRecipes/' + recipe_category]).decode("utf-8").split('\n')
        for recipe_in_category in all_recipes_in_category:      
            if recipe_in_category != '':
                recipePath = '../allRecipes/' + recipe_category + '/' + recipe_in_category 

                recipe = import_json(recipePath)
                html = import_html(html_template_path)

                output_html_path = 'allRecipes/' + remove_spaces(recipe['recipeCategory'][0]) + '/' + remove_spaces(recipe['recipeName'][0]) + '.html'


                ingredients_html = create_ingredients_html(recipe['ingredients'])

                html = html.replace(category_tag, recipe['recipeCategory'][0])
                html = html.replace(name_tag, recipe['recipeName'][0])
                html = html.replace(notes_tag, 'Notes: ' + recipe['notes'][0])
                html = html.replace(directions_tag, recipe['directions'][0])
                html = html.replace(ingredients_tag, ingredients_html)

                subprocess.call(["mkdir", "-p", "allRecipes/" + remove_spaces(recipe['recipeCategory'][0])])

                export_html(output_html_path, html)


