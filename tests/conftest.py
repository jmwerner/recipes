'''Base configurations for tests'''

import os
import pytest
import bs4 as bs
import subprocess
import sys

sys.path.insert(0, 'generator')
import webpageGenerator as gen


@pytest.fixture(scope="session")
def sitemap_name():
    return 'sitemap.xml'

@pytest.fixture(scope="session")
def root_directory():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

@pytest.fixture(scope="session")
def xml_tag():
    return 'loc'

@pytest.fixture(scope="session")
def raw_sitemap(root_directory, sitemap_name):
    try:
        with open(root_directory + '/' + sitemap_name) as file:
            sitemap = file.read().replace('\n', '')
    except ValueError:
        print('Error: Specified sitemap does not exist')
    return sitemap

@pytest.fixture(scope="session")
def processed_links_from_sitemap(raw_sitemap, xml_tag):
    soup = bs.BeautifulSoup(raw_sitemap, 'lxml')
    sitemap_links = soup.findAll(xml_tag)
    all_links = []
    for i in range(0, len(sitemap_links)):
        stripped_link = strip_link(sitemap_links[i], xml_tag)
        all_links.append(stripped_link)
    return all_links

@pytest.fixture(scope="session")
def recipe_raw_folder_name():
    return 'allRecipes'

@pytest.fixture(scope="session")
def recipe_category_names(recipe_raw_folder_name):
    categories = []
    for folder in os.listdir(recipe_raw_folder_name):
        if not folder.startswith('.'):
            categories.append(folder)
    return categories


def strip_link(link_input, tag):
    link = str(link_input)
    link = link.replace('<' + tag + '>', '')
    link = link.replace('</' + tag + '>', '')
    link = link.strip()
    return link


class Helpers:
    @staticmethod
    def get_html_from_local_file(file):
        # Replace base website with local path for fast reading
        with open(file, "r") as f:
            page = f.read()
        return page

    @staticmethod
    def get_local_file_from_url(url, root_directory):
        return url.replace('http://jmwerner.github.io/recipes', root_directory)

    @staticmethod
    def create_category_iterator(ingredients_dict):
        unique_categories = ['']
        for i in range(0, len(ingredients_dict)):
            if 'category' in ingredients_dict[i]:
                if ingredients_dict[i]['category'][0] not in unique_categories:
                    unique_categories.append(ingredients_dict[i]['category'][0])
        if(len(unique_categories) == 1 and unique_categories[0] == ''):
            unique_categories = ['noCategory']
        output_dict = {}
        for key in unique_categories:
            output_dict[key] = 0
        return output_dict

    @staticmethod
    def find_ingredient_category(input):
        if 'category' not in input:
            return 'noCategory'
        else:
            if not input['category'][0]:
                return 'noCategory'
            else:
                return input['category'][0]

    @staticmethod
    def process_json_name(input_string):
        output_string = input_string.strip(' \n').lower().title()
        output_string = gen.lower_special_cases_in_string(output_string)
        output_string = gen.replace_degrees_in_string(output_string)
        return output_string

    @staticmethod
    def process_json_number(input_number):
        return gen.convert_to_mixed_number(input_number)

    @staticmethod
    def process_html_ingredient_name(input_string):
        output_string = input_string.replace('°', '&#176')
        return output_string

    @staticmethod
    def make_ingredient_dict_from_html(html):
        soup = bs.BeautifulSoup(html, 'lxml')
        ingredient_names_from_html = soup.find_all('span', \
            {'id': lambda L: L and L.startswith('recipeIngredient')})
        ingredient_numbers_from_html = soup.find_all('span', \
            {'id': lambda L: L and L.startswith('recipeNumber')})
        ingredient_units_from_html = soup.find_all('span', \
            {'id': lambda L: L and L.startswith('recipeUnit')})
        ingredient_dict = {}
        if ingredient_names_from_html:
            for i in range(0, len(ingredient_names_from_html)):
                ingredient_id = ingredient_names_from_html[i].get('id')
                ingredient_id = ingredient_id.replace('recipeIngredient-', '')
                ingredient_dict[ingredient_id] = \
                    {'name': ingredient_names_from_html[i].text.strip(' \n'), \
                    'number': ingredient_numbers_from_html[i].text.strip(' \n'), \
                    'units': ingredient_units_from_html[i].text.strip(' \n'), \
                    'value_tag':ingredient_numbers_from_html[i].get('value')}
        return ingredient_dict

    @staticmethod
    def convert_mixed_number_to_fraction(input_string):
        splits = input_string.split(' ')
        splits = [x for x in splits if x]
        if len(splits) not in [1, 2]:
            raise ValueError('Mixed number conversion failed due to improper form')
        if len(splits) == 1:
            inner_splits = splits[0].split('/')
            inner_splits = [x for x in inner_splits if x]
            if len(inner_splits) == 1:
                return (int(inner_splits[0]), 1)
            else:
                return (int(inner_splits[0]), int(inner_splits[1]))
        else:
            splits_new = splits[1].split(' ')
            splits_new = [x for x in splits_new if x]
            if len(splits_new) == 1:
                inner_splits_new = splits_new[0].split('/')
                inner_splits_new = [x for x in inner_splits_new if x]
                if len(inner_splits_new) == 1:
                    processed_touple = (int(inner_splits_new[0]), 1)
                else:
                    processed_touple = (int(inner_splits_new[0]), int(inner_splits_new[1]))
            output_numerator = processed_touple[0] + int(splits[0]) * processed_touple[1]
            return (output_numerator, processed_touple[1])

    @staticmethod
    def simplify_fraction(numer, denom):
        a = numer
        b = denom
        while b:
            a, b = b, a % b

        common_divisor = a

        (reduced_num, reduced_den) = \
            (numer / common_divisor, denom / common_divisor)
        if reduced_den == 1:
            return (int(reduced_num), int(reduced_den))
        elif common_divisor == 1:
            return (numer, denom)
        else:
            return (int(reduced_num), int(reduced_den))

    def process_json_units(self, input_list, scaling_number = '1'):
        scaling_number_fraction = self.convert_mixed_number_to_fraction(scaling_number)
        plural = (gen.string_to_float(input_list['number'][0]) * \
                  scaling_number_fraction[0] / scaling_number_fraction[1]) > 1.0
        processed_units = gen.set_plural_suffix(input_list['units'][0], plural)
        return processed_units

    def make_ingredient_dict_from_link(self, root_directory, link):
        html = self.get_html_from_local_file(self.get_local_file_from_url(link, root_directory))
        return self.make_ingredient_dict_from_html(html)

    def process_and_scale_json_number(self, input_number, scaling_number):
        mixed_number = gen.convert_to_mixed_number(input_number)
        input_number_fraction = self.convert_mixed_number_to_fraction(mixed_number)
        scaling_number_fraction = self.convert_mixed_number_to_fraction(scaling_number)
        scaled_fraction = (input_number_fraction[0] * scaling_number_fraction[0], \
                           input_number_fraction[1] * scaling_number_fraction[1])
        scaled_fraction = self.simplify_fraction(scaled_fraction[0], scaled_fraction[1])
        scaled_fraction_string = str(scaled_fraction[0]) + '/' + str(scaled_fraction[1])
        return gen.convert_to_mixed_number(scaled_fraction_string)



@pytest.fixture(scope="session")
def helpers():
    return Helpers