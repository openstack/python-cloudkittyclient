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


class SummaryManager(base.BaseManager):

    url = '/v2/summary'

    def get_summary(self, **kwargs):
        """Returns a paginated list of summaries.

        This support filters along with custom grouping.

        :param offset: Index of the first scope that should be returned.
        :type offset: int
        :param limit: Maximal number of scopes to return.
        :type limit: int
        :param filters: Optional dict of filters to select data on.
        :type filters: dict
        :param groupby: Optional list of attributes to group data on.
        :type groupby: str or list of str.
        :param begin: Start of the period to gather data from
        :type begin: datetime.datetime
        :param end: End of the period to gather data from
        :type end: datetime.datetime
        """
        if 'groupby' in kwargs.keys() and isinstance(kwargs['groupby'], list):
            kwargs['groupby'] = ','.join(kwargs['groupby'])

        kwargs['filters'] = ','.join(
            '{}:{}'.format(k, v) for k, v in
            (kwargs.get('filters', None) or {}).items()
        )

        authorized_args = [
            'offset', 'limit', 'filters', 'groupby', 'begin', 'end']

        url = self.get_url(None, kwargs, authorized_args=authorized_args)
        return self.api_client.get(url).json()
