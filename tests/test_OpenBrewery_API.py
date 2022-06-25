""" Tests for OpenBrewery DB API
"""
import constants as cs

import pytest
import random
import requests


def test_check_status_code_for_random_brewery():
    """ Test to check status code while getting random brewery.
    """
    random_url = "{host}/{breweries}/{random}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, random=cs.RANDOM_ENDPOINT)
    random_brewery = requests.get(random_url)

    assert random_brewery.status_code == 200, "Status code differs from expected"
	
	
def test_check_random_returned_record_is_unique():
    """ Test to check that returned record is unique every time you get a random brewery.
    """
    random_url = "{host}/{breweries}/{random}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, random=cs.RANDOM_ENDPOINT)
    random_list = []

    for _ in range(10):
        random_brewery = requests.get(random_url).json()[0]
        random_list.append(random_brewery["id"])

    assert len(random_list) == len(set(random_list))


def test_check_status_code_for_valid_single_brewery(get_random_brewery):
    """ Test to check status code while getting valid single brewery.
    """
    single_url = "{host}/{breweries}/{id}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, id=get_random_brewery["id"])
    single_brewery = requests.get(single_url)

    assert single_brewery.status_code == 200, "Status code differs from expected"
	
	
def test_check_returned_record_for_valid_single_brewery(get_random_brewery):
    """ Test to check returned record while getting valid single brewery.
    """
    single_url = "{host}/{breweries}/{id}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, id=get_random_brewery["id"])
    single_brewery = requests.get(single_url).json()

    assert single_brewery == get_random_brewery
	

def test_check_status_code_for_invalid_single_brewery(generate_random_string):
    """ Test to check status code while getting invalid single brewery.
    """
    single_url = "{host}/{breweries}/{id}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, id=generate_random_string)
    single_brewery = requests.get(single_url)

    assert single_brewery.status_code == 404, "Status code differs from expected"
	

def test_check_error_message_for_invalid_single_brewery(generate_random_string):
    """ Test to check error message while getting nonexistent single brewery.
    """
    single_url = "{host}/{breweries}/{id}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT, id=generate_random_string)
    single_brewery = requests.get(single_url).json()

    assert single_brewery["message"] == cs.NONEXISTENT_BREWERY_ERROR


def test_check_status_code_for_all_breweries():
    """ Test to check status code while getting all breweries.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    all_breweries = requests.get(breweries_url)

    assert all_breweries.status_code == 200, "Status code differs from expected"
	

def test_check_status_code_for_breweries_filtered_by_valid_city(get_random_brewery):
    """ Test to check status code while getting filtered breweries by existing city.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_city': get_random_brewery["city"]})

    assert filtered_breweries.status_code == 200, "Status code differs from expected"


def test_get_breweries_filtered_by_valid_city(get_random_brewery):	
    """ Test to filter all breweries by existing city.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_city': get_random_brewery["city"]}).json()
    # in that case filtering is based on occurrence of the word, NOT exact match
    for record in filtered_breweries:
        assert get_random_brewery["city"] in record["city"]
		

def test_check_status_code_for_breweries_filtered_by_invalid_city(generate_random_string):
    """ Test to check status code while getting filtered breweries by nonexisting city.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_city': generate_random_string})

    assert filtered_breweries.status_code == 200, "Status code differs from expected"
		
		
def test_get_breweries_filtered_by_invalid_city(generate_random_string):
    """ Test to filter all breweries by nonexistent city.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_city': generate_random_string}).json()

    assert filtered_breweries == []


@pytest.mark.parametrize("brewery_type, status_code", [(random.choice(cs.BREWERY_TYPES), 200),
                                                       ("invalid", 400),
                                                       (123456, 400)])
def test_check_status_code_for_breweries_filtered_by_type(brewery_type, status_code):
    """ Test to check status code while getting filtered breweries by type.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_type': brewery_type})
	
    assert filtered_breweries.status_code == status_code, "Status code differs from expected"
	
	
@pytest.mark.parametrize("brewery_type", [random.choice(cs.BREWERY_TYPES)])
def test_get_breweries_filtered_by_valid_type(brewery_type):
    """ Test to filter all breweries by valid type.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_type': brewery_type}).json()
    # in that case filtering is based on exact match
    for record in filtered_breweries:
        assert record["brewery_type"] == brewery_type
		
		
def test_get_breweries_filtered_by_invalid_type(generate_random_string):
    """ Test to filter all breweries by invalid type.
    """
    breweries_url = "{host}/{breweries}".format(host=cs.HOST, breweries=cs.BREWERIES_ENDPOINT)
    filtered_breweries = requests.get(breweries_url, params={'by_type': generate_random_string}).json()

    assert cs.INVALID_TYPE_ERROR in filtered_breweries["errors"][0]
