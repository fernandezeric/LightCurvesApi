import sys
import json

sys.path.append("..")

from app import app
from flask import json

def test_radio_degree():
    client = app.test_client()
    url = '/radio-degree'

    headers = {
        'content-type': 'application/json',
    }

    data = {
        'ra':'139.33444972',
        'dec':'68.6350604',
        'radius':'0.0002777',
        'format':'csv',
        'catalog':'ztf'
        }

    response = client.post(url, data=(data)) #data=json.dumps(data)
    assert response.status_code == 200

def test_radio_degree_nearest():
    client = app.test_client()
    url = '/radio-degree-nearest'

    headers = {
        'content-type': 'application/json',
    }

    data = {
        'ra':'139.33444972',
        'dec':'68.6350604',
        'radius':'0.0002777',
        'format':'csv',
        'catalog':'ztf'
        }

    response = client.post(url, data=(data)) #data=json.dumps(data)
    assert response.status_code == 200

def test_radio_hms():
    client = app.test_client()
    url = '/radio-hms'

    headers = {
        'content-type': 'application/json',
    }

    data =  {
        'hms':'9h17m20.26793280000689s +4h34m32.414496000003936s',
        'radius':'0.0002777',
        'format':'csv',
        'catalog':'ztf'
        }

    response = client.post(url, data=(data)) #data=json.dumps(data)
    assert response.status_code == 200

def test_radio_hms_nearest():
    client = app.test_client()
    url = '/radio-hms-nearest'

    headers = {
        'content-type': 'application/json',
    }

    data =  {
        'hms':'9h17m20.26793280000689s +4h34m32.414496000003936s',
        'radius':'0.0002777',
        'format':'csv',
        'catalog':'ztf'
        }

    response = client.post(url, data=(data)) #data=json.dumps(data)
    assert response.status_code == 200