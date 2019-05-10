# Copyright 2019 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
from cloudkittyclient.common import base


class ScopeManager(base.BaseManager):
    """Class used to handle /v2/scope endpoint"""

    url = '/v2/scope'

    def get_scope_state(self, **kwargs):
        """Returns a paginated list of scopes along with their state.

        Some optional filters can be provided.

        :param offset: Index of the first scope that should be returned.
        :type offset: int
        :param limit: Maximal number of scopes to return.
        :type limit: int
        :param collector: Optional collector to filter on.
        :type collector: str or list of str
        :param fetcher: Optional fetcher to filter on.
        :type fetcher: str or list of str
        :param scope_id: Optional scope_id to filter on.
        :type scope_id: str or list of str
        :param scope_key: Optional scope_key to filter on.
        :type scope_key: str or list of str
        """

        for key in ('collector', 'fetcher', 'scope_id', 'scope_key'):
            if key in kwargs.keys():
                if isinstance(kwargs[key], list):
                    kwargs[key] = ','.join(kwargs[key])

        authorized_args = [
            'offset', 'limit', 'collector', 'fetcher', 'scope_id', 'scope_key']
        url = self.get_url(None, kwargs, authorized_args=authorized_args)
        return self.api_client.get(url).json()
