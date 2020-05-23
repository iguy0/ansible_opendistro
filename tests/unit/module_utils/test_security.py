from httpretty import HTTPretty
import pytest
from ansible_collections.jiuka.opendistro.plugins.module_utils.security import SecurityApi


@pytest.fixture
def base_api(ansible_module):
    HTTPretty.register_uri(HTTPretty.GET, 'https://es:9200/_nodes/_local/plugins', body='{}',
                           headers={'Content-Type': 'application/json'})

    return SecurityApi(ansible_module, 'foobar')

def test_get(base_api):
    HTTPretty.register_uri(HTTPretty.GET, 'https://es:9200/_opendistro/_security/api/FOO/BAR', body='{}')

    code, data = base_api.get('FOO', 'BAR')

    assert HTTPretty.last_request.method == 'GET'
    assert HTTPretty.last_request.headers.get('User-Agent') == 'ansible-VERS/jiuka.opendistro.foobar'
    assert HTTPretty.last_request.path == '/_opendistro/_security/api/FOO/BAR'

    assert data == {}
