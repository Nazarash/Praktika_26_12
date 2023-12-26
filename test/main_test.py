import requests
import json
import pytest

BASE_URL = 'http://localhost:8000'

@pytest.mark.parametrize("entity_id", [1, 2, 3, 4, 5])
def test_get_existing_entity(entity_id):
    response = requests.get(f'{BASE_URL}/entities/{entity_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['data']['id'] == entity_id

@pytest.mark.parametrize("entity_id", [-1, 0, 999])
def test_get_non_existing_entity(entity_id):
    response = requests.get(f'{BASE_URL}/entities/{entity_id}')
    assert response.status_code == 200
    assert b'Entity not found' in response.content

@pytest.mark.parametrize("name", ["New Entity 1", "New Entity 2", "New Entity 3"])
def test_post_new_entity(name):
    headers = {'Content-Type': 'application/json'}
    data = {'name': name}
    response = requests.post(f'{BASE_URL}/entities', headers=headers, data=json.dumps(data))
    assert response.status_code == 201
    result = response.json()
    assert result['id'] is not None

@pytest.mark.parametrize("name", ["Entity for Testing 1", "Entity for Testing 2", "Entity for Testing 3"])
def test_post_new_entity_and_get_it(name):
    headers = {'Content-Type': 'application/json'}
    data = {'name': name}
    response_post = requests.post(f'{BASE_URL}/entities', headers=headers, data=json.dumps(data))
    assert response_post.status_code == 201
    result = response_post.json()
    assert result['id'] is not None

    entity_id = result['id']
    response_get = requests.get(f'{BASE_URL}/entities/{entity_id}')
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get['data']['id'] == entity_id
    assert data_get['data']['name'] == name

@pytest.mark.parametrize("invalid_endpoint", ["invalid_endpoint_1", "invalid_endpoint_2", "invalid_endpoint_3"])
def test_invalid_endpoint(invalid_endpoint):
    response = requests.get(f'{BASE_URL}/{invalid_endpoint}')
    assert response.status_code == 200

@pytest.mark.parametrize("invalid_entity_id", ["invalid_id_1", "invalid_id_2", "invalid_id_3"])
def test_get_invalid_entity_id(invalid_entity_id):
    response = requests.get(f'{BASE_URL}/entities/{invalid_entity_id}')
    assert response.status_code == 200
