from requests import post, get
from json import loads, dumps

import pytest


host = "http://lyceum_api:80"


def test_creating_school():
    test_name = "TEST"
    test_address = "TEST"
    post(f"{host}/school", json={"name": test_name,
                                 "address": test_address})
    response = get(f"{host}/school")
    mask = [x["name"] == test_name and x["address"] == test_address
            for x in response.json()["schools"]]
    assert any(mask)

