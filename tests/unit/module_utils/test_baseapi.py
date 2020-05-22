import pytest
from ansible_collections.jiuka.opendistro.plugins.module_utils.baseapi import BaseApi

@pytest.fixture
def base_api(ansible_module):
    return BaseApi(ansible_module, 'foobar')

def test_init(base_api):
    assert base_api

def test_http_agent(base_api):
    assert base_api._http_agent() == 'ansible-VERS/jiuka.opendistro.foobar'

def test_url(base_api):
    assert base_api.url('FOO', 'BAR') == 'https://es:9200/_opendistro/_None/api/FOO/BAR'

def test_url_wo_name(base_api):
    assert base_api.url('FOO') == 'https://es:9200/_opendistro/_None/api/FOO'
