import sys
#sys.path.append('/usr/share/ansible/collections')

def _import(name, *args, **kwargs):
    if name.startswith('ansible_collections.jiuka.opendistro.'):
        name = name[37:]
    return original_import(name, *args, **kwargs)

import builtins
original_import = builtins.__import__
builtins.__import__ = _import

import pytest

@pytest.fixture
def ansible_module():
    return MockModule()

class MockModule:
    def __init__(self, **kwargs):
        self.params = dict(
                elasticsearch_url='https://es:9200',
        )
        self.params.update(kwargs)
        self.ansible_version = 'VERS'
