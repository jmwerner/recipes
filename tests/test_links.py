import pytest
import requests

def test_links(processed_links):
    for link in processed_links:
        assert requests.get(link).ok

