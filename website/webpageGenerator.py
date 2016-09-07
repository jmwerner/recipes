
import json
import ast

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

recipePath = '../allRecipes/Breakfast/FluffyPancakes.json'
HTMLPath = 'templates/recipeTemplate.html'
outputHTMLPath = 'templates/recipe_test.html'


category_tag = '<RECIPE_CATEGORY_GOES_HERE>'
name_tag = '<RECIPE_NAME_GOES_HERE>'
notes_tag = '<RECIPE_NOTES_GOES_HERE>'
directions_tag = '<RECIPE_DIRECTIONS_GO_HERE>'
ingredients_tag = '<RECIPE_INGREDIENTS_GO_HERE>'


with open(recipePath, 'r') as recipe_file:
    recipe = json.load(recipe_file)

recipe_file.close()


with open(HTMLPath, 'r') as html_file:
    html = html_file.read()

html_file.close()


ingredients_html = create_ingredients_html(recipe['ingredients'])

html = html.replace(category_tag, recipe['recipeCategory'][0])
html = html.replace(name_tag, recipe['recipeName'][0])
html = html.replace(notes_tag, 'Notes: ' + recipe['notes'][0])
html = html.replace(directions_tag, recipe['directions'][0])
html = html.replace(ingredients_tag, ingredients_html)



with open(outputHTMLPath, 'w') as html_output_file:
  html_output_file.write(html)

html_output_file.close()


