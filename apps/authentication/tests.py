import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_signup():
    client = APIClient()
    
    url = '/api/user/signup/'
    payload = {
        'email': 'test@gmail.com',
        'password': 'asdf',
        'first_name': 'John',
        'second_name': 'Doe',
        'country': 'Nepal',
        'phone_number': '+9779860099345',
        'date_of_birth': '1998-12-12'
    }
    
    response = client.post(url, payload)
    assert response.status_code == 400