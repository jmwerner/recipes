import pytest
import bs4 as bs
import os

@pytest.fixture(scope="session")
def sitemap_name():
    return 'sitemap.xml'

@pytest.fixture(scope="session")
def base_url():
    return 'https://jmwerner.github.io/recipes/website/index.html'

@pytest.fixture(scope="session")
def xml_tag():
    return 'loc'

@pytest.fixture(scope="session")
def raw_sitemap(sitemap_name):
    try:
        with open(sitemap_name) as f:
            sitemap = f.read().replace('\n', '')
    except:
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

