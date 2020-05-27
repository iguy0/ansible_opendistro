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
module: role_info

short_description: Return role information.

version_added: "1.0.0"

description:
    - Return role information.

options:
    name:
        description:
            - Name of the role to fetch informations for.
        type: str
        required: true
        aliases: [ role ]

extends_documentation_fragment:
    - jiuka.opendistro.baseapi

author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
- name: Get admin
  jiuka.opendistor.role_info:
    name: admin
'''

RETURN = '''
role:
    description: Informations about the role.
    returned: if role exists
    type: dict
    contains:
        name:
            description: Name of the role.
            type: str
        description:
            description: Description of the role.
            type: str
        hidden:
            description: If the role is hidden.
            type: bool
        reserved:
            description: If the role is reserved.
            type: bool
        static:
            description: If the role is static.
            type: bool
        cluster_permissions:
            description: Cluster permissions of the role.
            type: list
            elements: str
        index_permissions:
            description: Index permissions of the role.
            type: list
            elements: dict
            contains:
                index_patterns:
                    description: Index patterns to apply permisions to.
                    type: list
                    elements: str
                fls:
                masked_fields:
                allowed_actions:
                    description: Allowed actions.
                    type: list
                    elements: str
        tenant_permissions
            description: Tenant permissions of the role.
            type: list
            elements: dict
            contains:
                tenant_patterns:
                    description: Tenant patterns to apply permisions to.
                    type: list
                    elements: str
                allowed_actions:
                    description: Allowed actions.
                    type: list
                    elements: str
'''


from ansible_collections.jiuka.opendistro.plugins.module_utils.basic import OpenDistroModule
from ansible_collections.jiuka.opendistro.plugins.module_utils.security import SecurityApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True, aliases=['role']),
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
    api = SecurityApi(module, 'jiuka.opendistro.role_info')
    result['server'] = api.server

    # Get current state
    code, data = api.get('roles', name)
    if code == 200:
        result['role'] = data[name]
        result['role']['name'] = name
        result['state'] = 'present'
        result['exists'] = True
    elif code == 404:
        result['state'] = 'present'
        result['exists'] = False
    else:
        module.fail_json(msg='Error fetching role infos',
                         http_code=code,
                         http_body=data,
                         **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()