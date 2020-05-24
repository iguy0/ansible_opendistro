# Copyright: (c) 2020, Marius Rieder <marius.rieder@scs.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.jiuka.opendistro.plugins.module_utils.basic import BaseApi


class SecurityApi(BaseApi):
    PLUGIN = 'security'
