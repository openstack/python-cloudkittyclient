# Copyright 2015 Objectif Libre
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

from cloudkittyclient.common import base


class ReportSummary(base.Resource):

    key = 'summary'

    def __init(self, tenant_id=None, res_type=None, begin=None,
               end=None, rate=None):
        self.tenant_id = tenant_id
        self.res_type = res_type
        self.begin = begin
        self.end = end
        self.rate = rate

    def __repr__(self):
        return "<Summary %s" % self._info


class ReportManager(base.CrudManager):

    base_url = "/v1/report"

    def list_tenants(self):
        return self.client.get(self.base_url + "/tenants").json()

    def get_total(self, tenant_id=None, begin=None, end=None,
                  service=None, all_tenants=False):
        url = self.base_url + "/total"
        filters = list()
        if tenant_id:
            filters.append("tenant_id=%s" % tenant_id)
        if begin:
            filters.append("begin=%s" % begin.isoformat())
        if end:
            filters.append("end=%s" % end.isoformat())
        if service:
            filters.append("service=%s" % service)
        if all_tenants:
            filters.append("all_tenants=%s" % all_tenants)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.get(url).json()


class ReportSummaryManager(ReportManager):

    resource_class = ReportSummary
    key = 'summary'
    collection_key = "summary"

    def get_summary(self, tenant_id=None, begin=None, end=None,
                    service=None, groupby=None, all_tenants=False):
        kwargs = {}
        if tenant_id:
            kwargs['tenant_id'] = tenant_id
        if begin:
            kwargs['begin'] = begin.isoformat()
        if end:
            kwargs['end'] = end.isoformat()
        if service:
            kwargs['service'] = service
        if groupby:
            kwargs['groupby'] = groupby
        if all_tenants:
            kwargs['all_tenants'] = all_tenants
        return super(ReportManager, self).list(**kwargs)
