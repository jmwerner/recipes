import pytest
import requests
import urllib.request
import bs4 as bs

####################
# Helper functions #
####################

def url_is_valid(url):
    return requests.get(url).ok

def get_html_from_url(url):
    url_open = urllib.request.urlopen(url)
    raw_page = url_open.read()
    page = raw_page.decode("utf8")
    url_open.close()
    return page

def get_page_links(html):
    links = []
    soup = bs.BeautifulSoup(html)
    for a in soup.find_all('a', href=True):
        if not a['href'].startswith('mailto:') and not a['href'].startswith('#'):
            links.append(a['href'])
    return list(set(links))

def remove_page_name_from_url(url):
    return url.rsplit('/', 1)[0]

# Assumes that all links on page are relative (which was a design choice I made early on)
def check_all_links_on_page(url):
    html = get_html_from_url(url)
    links = get_page_links(html)
    root_url = remove_page_name_from_url(url)
    for page_name in links:
        url_check = url_is_valid(root_url + '/' + page_name)
        if not url_check:
            print('ERROR: ' + root_url + '/' + page_name + ' is broken!')
        assert url_check

#########
# Tests #
#########

def test_sitemap_links(processed_links_from_sitemap):
    for link in processed_links_from_sitemap:
        url_check = url_is_valid(link) 
        if not url_check:
            print('ERROR: Sitemap link ' + link + ' is broken!')
        assert url_check

def test_homepage_links(base_url):
    check_all_links_on_page(base_url)

def test_category_page_links(base_url, recipe_category_names):
    homepage_root = remove_page_name_from_url(base_url)
    category_page_links = [str(homepage_root + '/allRecipes/' + '{0}' + '.html').format(i) for i in recipe_category_names]
    for category_page in category_page_links:
        check_all_links_on_page(category_page)

