import sys

sys.path.append("..")

from app import app

def test_hello():
    response = app.test_client().get('/')

    print(response.data)
    assert response.status_code == 200
    assert response.data == b'Buenos D\xc3\xadas, ChikiMan <3!'