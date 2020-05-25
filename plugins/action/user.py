# Copyright: (c) 2020, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_text, to_bytes

try:
    import bcrypt
    HAS_BCRYPT = True
except Exception:
    HAS_BCRYPT = False


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp, task_vars)

        password = self._task.args.get('password', None)

        new_module_args = self._task.args.copy()

        if password:
            if not HAS_BCRYPT:
                raise AnsibleActionFail("Python module bcrypt is required for the password parameter.")

            salt = bcrypt.gensalt(prefix=b'2a')
            pwhash = bcrypt.hashpw(to_bytes(password), salt)
            new_module_args['password'] = None
            new_module_args['password_hash'] = to_text(pwhash)

        result.update(self._execute_module(module_name='jiuka.opendistro.user',
                                           module_args=new_module_args,
                                           task_vars=task_vars))

        return result
