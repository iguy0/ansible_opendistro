#!/usr/bin/python
# Copyright: (c) 2019, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import json
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.urls import Request
import ansible.module_utils.six.moves.urllib.error as urllib_error


class BaseApi(object):
    PLUGIN = None

    def __init__(self, module, module_name):
        self._module = module
        self._module_name = module_name

        self._url = self._module.params.get('elasticsearch_url')

        self._connect()

    def put(self, ressource, name, data):
        pass

    def get(self, ressource, name):
        pass

    def delete(self, ressource, name):
        pass

    @classmethod
    def client_argument_spec(cls, spec=None):
        arg_spec = dict(
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
            validate_certs=dict(type='bool',
                                required=False,
                                default=True,
                                fallback=(env_fallback, ['ELASTICSEARCH_VALIDATE_CERTS'])),
        )
        if spec:
            arg_spec.update(spec)
        return arg_spec

    def _connect(self):
        self.request = Request(
            headers={'Accept': 'application/json'},
            http_agent=self._http_agent(),
            url_username=self._module.params.get('elasticsearch_username'),
            url_password=self._module.params.get('elasticsearch_password'),
            force_basic_auth=True,
            validate_certs=self._module.params.get('validate_certs'),
        )

        self._server_info()

    def _server_info(self):
        self.server = {}

    def _http_agent(self):
        return 'ansible-{}/jiuka.opendistro.{}'.format(self._module.ansible_version,
                                                       self._module_name)

    def url(self, ressource, name=None):
        if name:
            return '{}/_opendistro/_{}/api/{}/{}'.format(self._url, self.PLUGIN, ressource, name)
        return '{}/_opendistro/_{}/api/{}'.format(self._url, self.PLUGIN, ressource)

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

        try:
            data = json.loads(data)
        except:
            data = body

        return code, data
