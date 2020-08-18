import sys

sys.path.append("..")

from app import app

def test_base_route():
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.get_data() == b'Buenos D\xc3\xadas, ChikiMan <3!'
    assert response.status_code == 200