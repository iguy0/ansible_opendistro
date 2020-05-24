#!/usr/bin/python
# Copyright: (c) 2020, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
module: user_info
short_description: Return user information.
version_added: "1.0.0"
description:
    - Return user information.
options:
    name:
        description:
            - Name of the user to fetch informations for.
        type: str
        required: true
        aliases: [ user ]
extends_documentation_fragment:
    - jiuka.opendistro.baseapi
author:
    - Marius Rieder (@jiuks)
'''

EXAMPLES = '''
- name: Get admin
  jiuka.opendistor.user_info:
    name: admin
'''

RETURN = '''
user:
    description: Informations about the user.
    returned: success
    type: dict
'''


from ansible_collections.jiuka.opendistro.plugins.module_utils.basic import OpenDistroModule
from ansible_collections.jiuka.opendistro.plugins.module_utils.security import SecurityApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True, aliases=['user']),
    )

    # seed the result dict in the object
    result = dict(
        changed=False,
    )

    # Setup AnsibleModule
    module = OpenDistroModule(
        argument_spec=module_args,
        supports_check_mode=True,
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
