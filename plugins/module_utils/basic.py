# Copyright: (c) 2020, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os.path
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.urls import Request
import ansible.module_utils.six.moves.urllib.error as urllib_error


class OpenDistroModule(AnsibleModule):
    def __init__(self, argument_spec, **kwargs):
        argument_spec.update(dict(
            elasticsearch_url=dict(type='str',
                                   required=False,
                                   fallback=(env_fallback, ['ELASTICSEARCH_URL'])),
            elasticsearch_user=dict(type='str',
                                    required=False,
                                    fallback=(env_fallback, ['ELASTICSEARCH_USER'])),
            elasticsearch_password=dict(type='str',
                                        required=False,
                                        no_log=True,
                                        fallback=(env_fallback, ['ELASTICSEARCH_PASSWORD'])),
            elasticsearch_cert=dict(type='path',
                                    required=False,
                                    fallback=(env_fallback, ['ELASTICSEARCH_CERT'])),
            elasticsearch_key=dict(type='path',
                                   required=False,
                                   fallback=(env_fallback, ['ELASTICSEARCH_KEY'])),
            elasticsearch_cacert=dict(type='path',
                                      required=False,
                                      fallback=(env_fallback, ['ELASTICSEARCH_CACERT'])),
            validate_certs=dict(type='bool',
                                required=False,
                                default=True,
                                fallback=(env_fallback, ['ELASTICSEARCH_VALIDATE_CERTS'])),
        ))
        required_together = kwargs.get('required_together', [])
        required_together += [
            ['elasticsearch_user', 'elasticsearch_password'],
            ['elasticsearch_cert', 'elasticsearch_key'],
        ]
        kwargs['required_together'] = required_together

        super().__init__(argument_spec, **kwargs)

        if not self.params['elasticsearch_url']:
            self.fail_json(msg="missing required arguments: elasticsearch_url")

        for param in ['elasticsearch_cert', 'elasticsearch_key', 'elasticsearch_cacert']:
            if not self.params.get(param, None):
                continue
            if os.path.exists(self.params[param]):
                continue
            self.fail_json(msg='{0} "{1}" not found'.format(param, self.params[param]))


class BaseApi(object):
    PLUGIN = None

    def __init__(self, module, module_name):
        self._module = module
        self._module_name = module_name

        self._es_url = self._module.params.get('elasticsearch_url')

        self._connect()

    def put(self, ressource, name=None, data=None):
        return self._open('PUT', self._url(ressource, name), data=data)

    def get(self, ressource, name=None):
        return self._open('GET', self._url(ressource, name))

    def delete(self, ressource, name=None):
        return self._open('DELETE', self._url(ressource, name))

    def _connect(self):
        self.request = Request(
            headers={'Accept': 'application/json'},
            http_agent=self._http_agent(),
            url_username=self._module.params.get('elasticsearch_user', None),
            url_password=self._module.params.get('elasticsearch_password', None),
            client_cert=self._module.params.get('elasticsearch_cert', None),
            client_key=self._module.params.get('elasticsearch_key', None),
            ca_path=self._module.params.get('elasticsearch_cacert', None),
            force_basic_auth=True,
            validate_certs=self._module.params.get('validate_certs'),
        )

        self._server_info()

    def _server_info(self):
        code, data = self._open('GET', '{0}/_nodes/_local/plugins'.format(self._es_url))

        if code != 200 or 'nodes' not in data:
            self._module.fail_json(msg='Error talking to Elasticsearch {0}'.format(self._es_url),
                                   http_code=code,
                                   http_body=data)

        self.server = {}

    def _http_agent(self):
        return 'ansible-{0}/jiuka.opendistro.{1}'.format(self._module.ansible_version,
                                                         self._module_name)

    def _url(self, ressource, name=None):
        if name:
            return '{0}/_opendistro/_{1}/api/{2}/{3}'.format(self._es_url, self.PLUGIN, ressource, name)
        return '{0}/_opendistro/_{1}/api/{2}'.format(self._es_url, self.PLUGIN, ressource)

    def _open(self, method, url, data=None):
        headers = None

        if data:
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(data)

        try:
            resp = self.request.open(method, url, data=data, headers=headers)

            code = resp.code
            body = resp.read()
        except urllib_error.HTTPError as e:
            code = e.code
            try:
                body = e.read()
            except AttributeError:
                body = ''
        except urllib_error.URLError as e:
            self._module.fail_json(msg=str(e.reason),
                                   method=method,
                                   url=url,
                                   data=data)

        try:
            data = json.loads(body)
        except Exception:
            data = body

        return code, data
