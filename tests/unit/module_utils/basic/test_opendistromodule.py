import pytest
from unittest.mock import patch

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jiuka.opendistro.plugins.module_utils.basic import OpenDistroModule


@pytest.fixture(autouse=True)
def mocker():
    AnsibleModule.params = dict(elasticsearch_url=True)
    yield


@pytest.fixture
def mock_init_method():
    with patch.object(AnsibleModule, '__init__') as mock_method:
        yield mock_method


@pytest.fixture
def mock_fail_json_method():
    with patch.object(AnsibleModule, 'fail_json') as mock_method:
        yield mock_method


@pytest.mark.parametrize('param', [
    'elasticsearch_url',
    'elasticsearch_user', 'elasticsearch_password',
    'elasticsearch_cert', 'elasticsearch_key',
    'elasticsearch_cacert'])
def test_argument_spec(mock_init_method, param):
    OpenDistroModule({})
    assert param in mock_init_method.call_args[0][0]


@pytest.mark.parametrize('required_together', [
    ['foo', 'bar'],
    ['elasticsearch_user', 'elasticsearch_password'],
    ['elasticsearch_cert', 'elasticsearch_key']])
def test_required_together(mock_init_method, required_together):
    OpenDistroModule({}, required_together=[['foo', 'bar']])
    assert required_together in mock_init_method.call_args[1]['required_together']


def test_no_url(mock_init_method, mock_fail_json_method):
    AnsibleModule.params = dict(elasticsearch_url=None)
    OpenDistroModule({})
    mock_fail_json_method.assert_called_with(msg='missing required arguments: elasticsearch_url')
