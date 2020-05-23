#!/usr/bin/python

# Copyright: (c) 2019, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jiuka.opendistro.plugins.module_utils.security import SecurityApi

def main():
    # define available arguments/parameters a user can pass to the module
    module_args = SecurityApi.client_argument_spec(dict(
        name=dict(type='str', required=True, aliases=['user']),
    ))

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # Setup AnsibleModule
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Parameters
    name = module.params['name']

    # Setup API
    api = SecurityApi(module, 'jiuka.opendistro.user_info')
    result['server'] = api.server

    # Get current state
    code, data = api.get('internalusers', name)
    if code == 200:
        result['user'] = data
        result['state'] = 'present'
        result['exists'] = True
    elif code == 404:
        result['state'] = 'present'
        result['exists'] = False
    else:
        module.fail_json(msg='Error fetching user infos',
                         http_code=code,
                         http_body=data,
                         **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
