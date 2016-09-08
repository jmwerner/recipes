
import json
import ast
import subprocess

category_tag = '<RECIPE_CATEGORY_GOES_HERE>'
name_tag = '<RECIPE_NAME_GOES_HERE>'
notes_tag = '<RECIPE_NOTES_GOES_HERE>'
directions_tag = '<RECIPE_DIRECTIONS_GO_HERE>'
ingredients_tag = '<RECIPE_INGREDIENTS_GO_HERE>'
category_links_tag = '<RECIPE_CATEGORY_LINKS_GO_HERE>'
recipe_links_tag = '<RECIPE_LINKS_GO_HERE>'


recipe_html_template_path = 'templates/recipeTemplate.html'
index_html_template_path = 'templates/indexTemplate.html'
category_html_template_path = 'templates/categoryTemplate.html'


def create_ingredients_html(ingredients):
    output_html_string = '<ul>' + '\n'
    ingredients_list = ast.literal_eval(ingredients[0])
    for i in range(0, len(ingredients_list)):
        if ingredients_list[i]['name'][0] != '':
            output_html_string += '<li>' + ingredients_list[i]['number'][0] + \
                ' ' + ingredients_list[i]['units'][0] + ' ' + \
                ingredients_list[i]['name'][0] +  '</li>' + '\n'
    output_html_string += '</ul>' + '\n'
    return output_html_string

def create_category_link_html(categories):
    output_html_string = ''
    for i in range(0, len(categories)):
        output_html_string += '<a href=\"http://jmwerner.github.io/recipes/website/' + \
            categories[i] + '.html\"><h3>' + categories[i] + '</h3></a>\n'
    return output_html_string

def create_recipes_in_category_link_html(category, recipes_in_category):
    output_html_string = ''
    for i in range(0, len(recipes_in_category)):
        output_html_string += '<a href=\"http://jmwerner.github.io/recipes/website/allRecipes/' + \
            category + '/' + recipes_in_category[i] + '.html\"><h3>' + recipes_in_category[i] + '</h3></a>\n'
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
# Create recipes pages & category pages
################################################################################

all_categories = subprocess.check_output(['ls', '../allRecipes']).decode("utf-8").split('\n')
all_categories = [x for x in all_categories if x]

for recipe_category in all_categories:
    all_recipes_in_category = subprocess.check_output(['ls', '../allRecipes/' + recipe_category]).decode("utf-8").split('\n')
    all_recipes_in_category = [x for x in all_recipes_in_category if x]

    category_html = import_html(category_html_template_path)

    recipes_in_category_html = create_recipes_in_category_link_html(recipe_category, all_recipes_in_category)

    category_html = category_html.replace(category_tag, recipe_category)
    category_html = category_html.replace(recipe_links_tag, recipes_in_category_html)

    export_html('allRecipes/' + recipe_category + '.html', category_html)

    for recipe_in_category in all_recipes_in_category:      
        recipePath = '../allRecipes/' + recipe_category + '/' + recipe_in_category 

        recipe = import_json(recipePath)
        recipe_html = import_html(recipe_html_template_path)

        output_recipe_html_path = 'allRecipes/' + remove_spaces(recipe['recipeCategory'][0]) + '/' + remove_spaces(recipe['recipeName'][0]) + '.html'


        ingredients_html = create_ingredients_html(recipe['ingredients'])

        recipe_html = recipe_html.replace(category_tag, recipe['recipeCategory'][0])
        recipe_html = recipe_html.replace(name_tag, recipe['recipeName'][0])
        recipe_html = recipe_html.replace(notes_tag, 'Notes: ' + recipe['notes'][0])
        recipe_html = recipe_html.replace(directions_tag, recipe['directions'][0])
        recipe_html = recipe_html.replace(ingredients_tag, ingredients_html)

        subprocess.call(["mkdir", "-p", "allRecipes/" + remove_spaces(recipe['recipeCategory'][0])])

        export_html(output_recipe_html_path, recipe_html)

################################################################################
# Create home page
################################################################################

index_html = import_html(index_html_template_path)

categories_html = create_category_link_html(all_categories)
index_html = index_html.replace(category_links_tag, categories_html)

export_html('index.html', index_html)



