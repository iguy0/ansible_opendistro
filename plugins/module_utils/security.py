#!/usr/bin/python
# Copyright: (c) 2019, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import json
from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.urls import Request
import ansible.module_utils.six.moves.urllib.error as urllib_error

from ansible_collections.jiuka.opendistro.plugins.module_utils.baseapi import BaseApi

class SecurityApi(BaseApi):
    PLUGIN = 'security'

