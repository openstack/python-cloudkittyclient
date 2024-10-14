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
from oslo_utils import strutils

from cloudkittyclient.common import base
from cloudkittyclient import exc


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

    def reset_scope_state(self, **kwargs):
        """Returns nothing.

        Some optional filters can be provided.
        The all_scopes and the scope_id options are mutually exclusive and one
        must be provided.

        :param state: datetime object from which the state will be reset
        :type state: datetime.datetime
        :param all_scopes: Whether all scopes must be reset
        :type all_scopes: bool
        :param collector: Optional collector to filter on.
        :type collector: str or list of str
        :param fetcher: Optional fetcher to filter on.
        :type fetcher: str or list of str
        :param scope_id: Optional scope_id to filter on.
        :type scope_id: str or list of str
        :param scope_key: Optional scope_key to filter on.
        :type scope_key: str or list of str
        """

        if not kwargs.get('state'):
            raise exc.ArgumentRequired("'state' argument is required")

        if not kwargs.get('all_scopes') and not kwargs.get('scope_id'):
            raise exc.ArgumentRequired(
                "You must specify either 'scope_id' or 'all_scopes'")

        if kwargs.get('all_scopes') and kwargs.get('scope_id'):
            raise exc.InvalidArgumentError(
                "You can't specify both 'scope_id' and 'all_scopes'")

        for key in ('collector', 'fetcher', 'scope_id', 'scope_key'):
            if key in kwargs.keys():
                if isinstance(kwargs[key], list):
                    kwargs[key] = ','.join(kwargs[key])

        body = dict(
            state=kwargs.get('state'),
            scope_id=kwargs.get('scope_id'),
            scope_key=kwargs.get('scope_key'),
            collector=kwargs.get('collector'),
            fetcher=kwargs.get('fetcher'),
            all_scopes=kwargs.get('all_scopes'),
        )
        # Stripping None and False values
        body = dict(filter(lambda elem: bool(elem[1]), body.items()))

        url = self.get_url(None, kwargs)
        return self.api_client.put(url, json=body)

    def update_scope(self, **kwargs):
        """Update storage scope

        The `scope_id field` is mandatory, and all other are optional. Only the
        attributes sent will be updated. The attributes that are not sent will
        not be changed in the backend.

        :param collector: collector to be used by the scope.
        :type collector: str
        :param fetcher: fetcher to be used by the scope.
        :type fetcher: str
        :param scope_id: Mandatory scope_id to update.
        :type scope_id: str
        :param scope_key: scope_key to be used by the scope.
        :type scope_key: str
        :param active: Indicates if the scope is active or not
        :type active: str
        """

        if not kwargs.get('scope_id'):
            raise exc.ArgumentRequired("'scope_id' argument is required")

        body = dict(
            scope_id=kwargs.get('scope_id'),
            scope_key=kwargs.get('scope_key'),
            collector=kwargs.get('collector'),
            fetcher=kwargs.get('fetcher')
        )

        if kwargs.get('active'):
            body['active'] = strutils.bool_from_string(
                kwargs.get('active'), strict=True)

        # Stripping None
        body = dict(filter(lambda elem: elem[1] is not None, body.items()))

        url = self.get_url(None, kwargs)
        return self.api_client.patch(url, json=body).json()
