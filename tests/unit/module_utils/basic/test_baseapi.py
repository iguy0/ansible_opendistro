from httpretty import HTTPretty
import pytest
from ansible_collections.jiuka.opendistro.plugins.module_utils.basic import BaseApi


@pytest.fixture
def base_api(ansible_module):
    HTTPretty.register_uri(HTTPretty.GET, 'https://es:9200/_nodes/_local/plugins', body='{}',
                           headers={'Content-Type': 'application/json'})

    return BaseApi(ansible_module, 'foobar')


def test_init(base_api):
    assert base_api

    assert HTTPretty.last_request.method == 'GET'
    assert HTTPretty.last_request.headers.get('User-Agent') == 'ansible-VERS/jiuka.opendistro.foobar'


def test_http_agent(base_api):
    assert base_api._http_agent() == 'ansible-VERS/jiuka.opendistro.foobar'


def test_url(base_api):
    assert base_api._url('FOO', 'BAR') == 'https://es:9200/_opendistro/_None/api/FOO/BAR'


def test_url_wo_name(base_api):
    assert base_api._url('FOO') == 'https://es:9200/_opendistro/_None/api/FOO'


def test_put(base_api):
    HTTPretty.register_uri(HTTPretty.PUT, 'https://es:9200/_opendistro/_None/api/FOO/BAR', body='{}')

    code, data = base_api.put('FOO', 'BAR', {})

    assert HTTPretty.last_request.method == 'PUT'
    assert HTTPretty.last_request.headers.get('User-Agent') == 'ansible-VERS/jiuka.opendistro.foobar'
    assert HTTPretty.last_request.path == '/_opendistro/_None/api/FOO/BAR'

    assert data == {}


def test_get(base_api):
    HTTPretty.register_uri(HTTPretty.GET, 'https://es:9200/_opendistro/_None/api/FOO/BAR', body='{}')

    code, data = base_api.get('FOO', 'BAR')

    assert HTTPretty.last_request.method == 'GET'
    assert HTTPretty.last_request.headers.get('User-Agent') == 'ansible-VERS/jiuka.opendistro.foobar'
    assert HTTPretty.last_request.path == '/_opendistro/_None/api/FOO/BAR'

    assert data == {}


def test_get_wo_name(base_api):
    HTTPretty.register_uri(HTTPretty.GET, 'https://es:9200/_opendistro/_None/api/FOO', body='{}')

    code, data = base_api.get('FOO')

    assert HTTPretty.last_request.method == 'GET'
    assert HTTPretty.last_request.path == '/_opendistro/_None/api/FOO'

    assert data == {}


def test_get_error(base_api):
    HTTPretty.register_uri(HTTPretty.GET, 'https://es:9200/_opendistro/_None/api/FOO', body='{}', status=500)

    code, data = base_api.get('FOO')

    assert code == 500
    assert data == {}


def test_delete(base_api):
    HTTPretty.register_uri(HTTPretty.DELETE, 'https://es:9200/_opendistro/_None/api/FOO/BAR', body='{}')

    code, data = base_api.delete('FOO', 'BAR')

    assert HTTPretty.last_request.method == 'DELETE'
    assert HTTPretty.last_request.headers.get('User-Agent') == 'ansible-VERS/jiuka.opendistro.foobar'
    assert HTTPretty.last_request.path == '/_opendistro/_None/api/FOO/BAR'
