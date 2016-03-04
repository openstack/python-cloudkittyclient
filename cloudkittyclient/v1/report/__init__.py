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


class ReportResult(base.Resource):

    key = 'report'

    def __repr__(self):
        return "<Report %s>" % self._info


class ReportManager(base.Manager):

    base_url = "/v1/report"

    def list_tenants(self):
        return self.client.get(self.base_url + "/tenants").json()

    def get_total(self, tenant_id=None, begin=None, end=None, service=None):
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
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.get(url).json()
