import pytest
import bs4 as bs
import os.path

####################
# Helper functions #
####################

def get_page_links(html):
    links = []
    soup = bs.BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if not a['href'].startswith('mailto:') and not \
            a['href'].startswith('#'):
            links.append(a['href'])
    return list(set(links))

def remove_page_name_from_url(url):
    return url.rsplit('/', 1)[0]

#########
# Tests #
#########

def test_sitemap_links(processed_links_from_sitemap, root_directory, helpers):
    for link in processed_links_from_sitemap:
        url_check = os.path.isfile(helpers.get_local_file_from_url(link, root_directory))
        if not url_check:
            print('ERROR: Sitemap link ' + link + ' is broken!')
        assert url_check

def test_all_page_relative_links(root_directory, helpers):
    html = helpers.get_html_from_local_file(root_directory + '/website/index.html')
    links = get_page_links(html)
    links.remove('index.html')
    # Check all links on the homepage
    for page_name in links:
        url_check = os.path.isfile(root_directory + '/website/' + page_name)
        if not url_check:
            print('ERROR: ' + page_name + '\n on the homepage is broken!')
        assert url_check
        category_html = helpers.get_html_from_local_file(root_directory + '/website/' + page_name)
        category_links = get_page_links(category_html)
        # Check all links on category pages
        for category_page_name in category_links:
            category_url_check = os.path.isfile(root_directory + '/website/allRecipes/' + category_page_name)
            assert category_url_check
            # Check all links on recipe pages within a category
            category_page_name_splits = category_page_name.split('/')
            if len(category_page_name_splits) == 2:            
                recipe_html = helpers.get_html_from_local_file(root_directory + '/website/allRecipes/' + category_page_name)
                recipe_links = get_page_links(recipe_html)
                for recipe_page_name in recipe_links:
                    recipe_url_check = os.path.isfile(root_directory + '/website/allRecipes/' + category_page_name.split('/')[0] + '/' + recipe_page_name)
                    assert recipe_url_check

