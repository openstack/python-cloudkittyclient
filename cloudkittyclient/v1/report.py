# -*- coding: utf-8 -*-
# Copyright 2018 Objectif Libre
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
from oslo_log import log

from cloudkittyclient.common import base


LOG = log.getLogger(__name__)


class ReportManager(base.BaseManager):
    """Class used to handle /v1/report endpoint."""
    url = '/v1/report/{endpoint}'

    def get_summary(self, **kwargs):
        """Returns a list of summaries.

        :param begin: Begin timestamp
        :type begin: datetime.datetime
        :param end: End timestamp
        :type end: datetime.datetime
        :param tenant_id: Tenant ID
        :type tenant_id: str
        :param groupby: Fields to group by.
        :type groupby: list
        :param all_tenants: Get summary from all tenants (admin only). Defaults
                            to False.
        :type all_tenants: bool
        """
        authorized_args = [
            'begin', 'end', 'tenant_id', 'service', 'groupby', 'all_tenants']
        if kwargs.get('groupby', None):
            kwargs['groupby'] = ','.join(kwargs['groupby'])
        url = self.get_url('summary', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def get_total(self, **kwargs):
        """Returns the total for the given tenant.

        :param begin: Begin timestamp
        :type begin: datetime.datetime
        :param end: End timestamp
        :type end: datetime.datetime
        :param tenant_id: Tenant ID
        :type tenant_id: str
        :param all_tenants: Get total from all tenants (admin only). Defaults
                            to False.
        :type all_tenants: bool
        """
        LOG.warning('WARNING: /v1/report/total/ endpoint is deprecated, '
                    'please use /v1/report/summary instead.')
        authorized_args = [
            'begin', 'end', 'tenant_id', 'service', 'all_tenants']
        url = self.get_url('total', kwargs, authorized_args)
        return self.api_client.get(url).json()

    def get_tenants(self, **kwargs):
        """Returns a list of tenants.

        :param begin: Begin timestamp
        :type begin: datetime.datetime
        :param end: End timestamp
        :type end: datetime.datetime
        """
        url = self.get_url('tenants', kwargs, ['begin', 'end'])
        return self.api_client.get(url).json()
