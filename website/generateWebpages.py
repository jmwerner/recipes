
import json

recipePath = '../allRecipes/Breakfast/FluffyPancakes.json'
HTMLPath = 'templates/recipeTemplate.html'
outputHTMLPath = 'templates/recipe_test.html'


with open(recipePath, 'r') as recipe_file:
    recipe = json.load(recipe_file)

recipe_file.close()


with open(HTMLPath, 'r') as html_file:
    html = html_file.read()

html_file.close()








with open(outputHTMLPath, 'w') as html_file:
  html_file.write(html)

html_file.close()


