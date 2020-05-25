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
module: user

short_description: Manage OpenDistro Security users

version_added: "1.0.0"

description:
    - Manage user in a openDistro elasticsearch with security enabled.

options:
    name:
        description:
            - Name of the user to manage.
        type: str
        required: true
        aliases: [ user ]
    password:
        description:
            - Plaintext password to set for the user.
        type: str
        required: false
    password_hash:
        description:
            - BCrypt hashed password to set for the user.
        type: str
        required: false
        aliases: [ hash ]
    update_password:
        description:
            - Should the password be updated on each run?
        type: bool
        default: false
    description:
        description:
            - Description of the user.
        type: str
        required: false
    roles:
        description:
            - List of backend roles to assign the user to.
        type: list
        required: false
    attributes:
        description:
            - Dictonary of attributes to set for the user.
        type: dict
        required: false
    state:
        description:
            - The desired state of the user.
        type: str
        required: false
        choices: [ present, absent ]
        default: present

extends_documentation_fragment:
    - jiuka.opendistro.baseapi
author:
    - Marius Rieder (@jiuka)
'''

EXAMPLES = '''
- name: Create Foo user
  jiuka.opendistor.user_info:
    name: admin
'''

RETURN = '''
user:
    description: Informations about the user.
    returned: success
    type: dict
'''


from ansible_collections.jiuka.opendistro.plugins.module_utils.basic import OpenDistroModule, create_patch, apply_patch
from ansible_collections.jiuka.opendistro.plugins.module_utils.security import SecurityApi


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True, aliases=['user']),
        password=dict(type='str', required=False, no_log=True),
        password_hash=dict(type='str', required=False, aliases=['hash'], no_log=True),
        update_password=dict(type='bool',
                             required=False,
                             default=False, no_log=False),
        description=dict(type='str', required=False),
        roles=dict(type='list', required=False),
        attributes=dict(type='dict', required=False),
        state=dict(type='str',
                   default='present',
                   choices=['present', 'absent']),
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
    password = module.params['password']
    password_hash = module.params['password_hash']
    update_password = module.params['update_password']
    description = module.params['description']
    roles = module.params['roles']
    attributes = module.params['attributes']
    state = module.params['state']

    # Setup API
    api = SecurityApi(module, 'jiuka.opendistro.user')
    result['server'] = api.server

    # Get current state
    code, data = api.get('internalusers', name)
    if code == 200:
        current_config = data[name]
        current_state = 'present'
    elif code == 404:
        current_config = {}
        current_state = 'absent'
    else:
        module.fail_json(msg='Error fetching user infos',
                         http_code=code,
                         http_body=data,
                         **result)

    # Create
    if state == 'present' and current_state == 'absent':
        result['changed'] = True
        payload = dict()
        if password:
            payload['password'] = password
        elif password_hash:
            payload['hash'] = password_hash
        else:
            module.fail_json(msg='password or password_hash is mandatory to create a user.')

        if description:
            payload['description'] = description
        if roles:
            payload['backend_roles'] = roles

        if not module.check_mode:
            code, data = api.put('internalusers', name, data=payload)

            if code != 201:
                module.fail_json(msg='Error creating user',
                                 http_code=code,
                                 http_body=data,
                                 **result)

            code, data = api.get('internalusers', name)
            if code != 200:
                module.fail_json(msg='Error fetching user infos',
                                 http_code=code,
                                 http_body=data,
                                 **result)
            new_config = data[name]
        else:
            new_config = payload

    # Update
    if state == 'present' and current_state == 'present':
        payload = list(filter(None, [
            create_patch(current_config, 'description', description),
            create_patch(current_config, 'backend_roles', roles),
            create_patch(current_config, 'attributes', attributes),
        ]))

        if update_password:
            if password:
                payload.append(create_patch(current_config, 'password', password))
            else:
                payload.append(create_patch(current_config, 'hash', password_hash))

        if payload:
            result['changed'] = True

            if not module.check_mode:
                code, data = api.patch('internalusers', name, data=payload)

                if code != 200:
                    module.fail_json(msg='Error updating user',
                                     http_code=code,
                                     http_body=data,
                                     **result)

                code, data = api.get('internalusers', name)
                if code != 200:
                    module.fail_json(msg='Error fetching user infos',
                                     http_code=code,
                                     http_body=data,
                                     **result)
                new_config = data[name]
            else:
                new_config = current_config.copy()
                apply_patch(new_config, payload)

    # Delete
    if state == 'absent' and current_state == 'present':
        result['changed'] = True
        if not module.check_mode:
            code, data = api.delete('internalusers', name)
            if code != 200:
                module.fail_json(msg='Error deleting user',
                                 http_code=code,
                                 http_body=data,
                                 **result)
        new_config = {}

    if module._diff and result['changed']:
        result['diff'] = dict(
            before=current_config,
            after=new_config,
        )

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
