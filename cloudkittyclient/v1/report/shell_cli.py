# Copyright 2016 Objectif Libre
#
# All Rights Reserved.
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

from osc_lib.command import command

from cloudkittyclient.v1.report import shell


class CliTotalGet(command.Command):
    def get_parser(self, prog_name):
        parser = super(CliTotalGet, self).get_parser(prog_name)
        parser.add_argument('-t', '--tenant-id',
                            help='Tenant id',
                            required=False,
                            dest='total_tenant_id')
        parser.add_argument('-b', '--begin',
                            help='Begin timestamp',
                            required=False)
        parser.add_argument('-e', '--end',
                            help='End timestamp',
                            required=False)
        parser.add_argument('-s', '--service',
                            help='Service Type',
                            required=False)
        parser.add_argument('-a', '--all-tenants',
                            default=False,
                            action="store_true",
                            dest='all_tenants',
                            help='Allows to get total from all tenants'
                                 ' (admin only).')
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_total_get(ckclient, parsed_args)


class CliReportTenantList(command.Command):
    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_report_tenant_list(ckclient, parsed_args)


class CliSummaryGet(command.Command):
    def get_parser(self, prog_name):
        parser = super(CliSummaryGet, self).get_parser(prog_name)
        parser.add_argument('-t', '--tenant-id',
                            help='Tenant id',
                            required=False,
                            dest='summary_tenant_id')
        parser.add_argument('-b', '--begin',
                            help='Begin timestamp',
                            required=False)
        parser.add_argument('-e', '--end',
                            help='End timestamp',
                            required=False)
        parser.add_argument('-s', '--service',
                            help='Service Type',
                            required=False)
        parser.add_argument('-g', '--groupby',
                            help=('Fields to groupby, separated by '
                                  'commas if multiple, now support '
                                  'res_type,tenant_id'),
                            required=False)
        parser.add_argument('-a', '--all-tenants',
                            default=False,
                            action="store_true",
                            dest='all_tenants',
                            help='Allows to get summary from all tenants'
                                 ' (admin only).')
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_summary_get(ckclient, parsed_args)
