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
import collections
from unittest import mock

from cloudkittyclient.tests.unit.v1 import base
from cloudkittyclient.v1 import report_cli


class TestReportCli(base.BaseAPIEndpointTestCase):

    def test_report_tenant_list(self):

        class DummyAPIClient(object):
            def get_tenants(*args, **kwargs):
                return ['ee530dfc-319a-438f-9d43-346cfef501d6',
                        '91743a9a-688b-4526-b568-7b501531176c',
                        '4468704c-972e-4cfd-a342-9b71c493b79b']

        class ClientWrap(object):
            report = DummyAPIClient()

        class DummyParsedArgs(object):
            def __init__(self):
                self.begin = '2042-01-01T00:00:00'
                self.end = '2042-12-01T00:00:00'

        class DummyCliTenantList(report_cli.CliTenantList):
            def __init__(self):
                pass

        def __get_client_from_osc(*args):
            return ClientWrap()

        parsed_args = DummyParsedArgs()
        cli_class_instance = DummyCliTenantList()

        with mock.patch('cloudkittyclient.utils.get_client_from_osc',
                        new=__get_client_from_osc):
            # NOTE(peschk_l): self is only used used to get a client so just we
            # just override __init__ in order to skip class instanciation. In
            # python3 we could just have passed None
            result = report_cli.CliTenantList.take_action(
                cli_class_instance, parsed_args)

        assert len(result) == 2
        assert result[0] == ('Tenant ID', )
        assert isinstance(result[1], collections.Iterable)

        for res in result[1]:
            assert isinstance(res, collections.Iterable)
