import pytest
from tests import common
from datetime import datetime
from meilisearch.errors import MeiliSearchApiError

def test_get_keys_default(client):
    """Tests if search and admin keys have been generated and can be retrieved."""
    keys = client.get_keys()
    assert isinstance(keys, dict)
    assert len(keys['results']) == 2
    assert 'actions' in keys['results'][0]
    assert 'indexes' in keys['results'][0]
    assert keys['results'][0]['key'] is not None
    assert keys['results'][1]['key'] is not None

def test_get_keys_with_parameters(client):
    """Tests if search and admin keys have been generated and can be retrieved."""
    keys = client.get_keys({'limit': 1})
    assert isinstance(keys, dict)
    assert len(keys['results']) == 1

def test_get_key(client, test_key):
    """Tests if a key can be retrieved."""
    key = client.get_key(test_key['key'])
    assert isinstance(key, dict)
    assert 'actions' in key
    assert 'indexes' in key
    assert key['createdAt'] is not None

def test_get_key_inexistent(client):
    """Tests getting a key that does not exists."""
    with pytest.raises(Exception):
        client.get_key('No existing key')

def test_create_keys_default(client, test_key_info):
    """Tests the creation of a key with no optional argument."""
    key = client.create_key(test_key_info)
    assert isinstance(key, dict)
    assert 'key' in key
    assert 'name' in key
    assert 'actions' in key
    assert 'indexes' in key
    assert key['key'] is not None
    assert key['name'] is not None
    assert key['expiresAt'] is None
    assert key['createdAt'] is not None
    assert key['updatedAt'] is not None
    assert key['key'] is not None
    assert key['actions'] == test_key_info['actions']
    assert key['indexes'] == test_key_info['indexes']

def test_create_keys_with_options(client, test_key_info):
    """Tests the creation of a key with arguments."""
    key = client.create_key(options={'description': test_key_info['description'], 'actions': test_key_info['actions'], 'indexes': test_key_info['indexes'], 'uid': '82acc342-d2df-4291-84bd-8400d3f05f06', 'expiresAt': datetime(2030, 6, 4, 21, 8, 12, 32).isoformat()[:-3]+'Z' })
    assert isinstance(key, dict)
    assert key['key'] is not None
    assert key['name'] is None
    assert key['description'] == test_key_info['description']
    assert key['expiresAt'] is not None
    assert key['createdAt'] is not None
    assert key['updatedAt'] is not None
    assert key['actions'] == test_key_info['actions']
    assert key['indexes'] == test_key_info['indexes']

def test_create_keys_with_wildcarded_actions(client, test_key_info):
    """Tests the creation of a key with an action which contains a wildcard."""
    key = client.create_key(options={'description': test_key_info['description'], 'actions': ['documents.*'], 'indexes': test_key_info['indexes'], 'expiresAt': None })

    assert isinstance(key, dict)
    assert key['actions'] == ['documents.*']

def test_create_keys_without_actions(client):
    """Tests the creation of a key with missing arguments."""
    with pytest.raises(MeiliSearchApiError):
        client.create_key(options={'indexes': [common.INDEX_UID]})

def test_update_keys(client, test_key_info):
    """Tests updating a key."""
    key = client.create_key(test_key_info)
    assert key['name'] == test_key_info['name']
    update_key = client.update_key(key_or_uid=key['key'], options={ 'name': 'keyTest' })
    assert update_key['key'] is not None
    assert update_key['expiresAt'] is None
    assert update_key['name'] == 'keyTest'

def test_delete_key(client, test_key):
    """Tests deleting a key."""
    resp = client.delete_key(test_key['key'])
    assert resp.status_code == 204
    with pytest.raises(MeiliSearchApiError):
        client.get_key(test_key['key'])

def test_delete_key_inexisting(client):
    """Tests deleting a key that does not exists."""
    with pytest.raises(MeiliSearchApiError):
        client.delete_key('No existing key')
