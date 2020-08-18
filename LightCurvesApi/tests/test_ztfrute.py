import sys
import json

sys.path.append("..")

from app import app
from flask import json


# def test_radio_degree():
#     params = {'ra':'139.33444972','dec':'68.6350604','radius':'0.0002777','format':'csv','catalog':'ztf'}
#     response = app.test_client().post(
#         '/radio-degree',
#         data = params
#         )
#     json_data = response.get_json()
#     assert response.status_code == 200

# def test_radio_degree_nearest():
#     params = {'ra':'139.33444972','dec':'68.6350604','radius':'0.0002777','format':'csv','catalog':'ztf'}
#     response = app.test_client().post(
#         '/radio-degree-nearest',
#         data = params
#         )
#     json_data = response.get_json()
#     assert response.status_code == 200

# def test_radio_hms():
#     params = {'hms':'9h17m20.26793280000689s +4h34m32.414496000003936s','radius':'0.0002777','format':'csv','catalog':'ztf'}
#     response = app.test_client().post(
#         '/radio-hms-nearest',
#         data = params
#         )
#     json_data = response.get_json()
#     assert response.status_code == 200

# def test_radio_hms_nearest():
#     params = {'hms':'9h17m20.26793280000689s +4h34m32.414496000003936s','radius':'0.0002777','format':'csv','catalog':'ztf'}
#     response = app.test_client().post(
#         '/radio-hms-nearest',
#         data = params
#         )
#     json_data = response.get_json()
#     assert response.status_code == 200


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

    response = client.post(url, data=json.dumps(data),headers=headers)
    assert response.status_code == 200
