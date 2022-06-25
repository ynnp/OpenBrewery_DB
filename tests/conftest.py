""" Module with fixtures
"""
import constants as cs

import pytest
import random
import requests
import string


@pytest.fixture()
def get_random_brewery():
    """ Function to get random brewery.

    :param: None
    :returns: brewery record
    :rtype: str
    """
    random_url = "{host}/{breweries}/{random}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, random=cs.RANDOM_ENDPOINT)
    random_brewery = requests.get(random_url).json()[0]

    return random_brewery
	
	
@pytest.fixture()
def generate_random_string():
    """ Function to generate random string for negative testing.
	
    :param: None
    :returns: random string
    :rtype: str
    """
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 50)))
