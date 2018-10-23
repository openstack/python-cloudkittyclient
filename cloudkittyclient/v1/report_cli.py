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
from cliff import lister
from cliff import show

from cloudkittyclient import exc
from cloudkittyclient import utils


class CliSummaryGet(lister.Lister):
    """Get a summary report."""
    summary_columns = [
        ('tenant_id', 'Tenant ID'),
        ('res_type', 'Resource Type'),
        ('rate', 'Rate'),
        ('begin', 'Begin Time'),
        ('end', 'End Time'),
    ]

    def take_action(self, parsed_args):
        for arg in ['begin', 'end']:
            value = getattr(parsed_args, arg)
            if value is not None:
                try:
                    setattr(parsed_args, arg, utils.iso2dt(value))
                except ValueError:
                    raise exc.InvalidArgumentError(
                        'Invalid timestamp "{}"'.format(value))
        resp = utils.get_client_from_osc(self).report.get_summary(
            **vars(parsed_args))
        values = utils.list_to_cols(
            resp.get('summary', []), self.summary_columns)
        return [col[1] for col in self.summary_columns], values

    def get_parser(self, prog_name):
        parser = super(CliSummaryGet, self).get_parser(prog_name)
        parser.add_argument('-t', '--tenant-id', type=str,
                            help='Tenant id.')
        parser.add_argument('-b', '--begin', type=str,
                            help='Begin timestamp.')
        parser.add_argument('-e', '--end', type=str,
                            help='End timestamp.')
        parser.add_argument('-s', '--service', type=str,
                            help='Service Type.')
        parser.add_argument('-g', '--groupby', nargs='+',
                            help='Fields to group by, space-separated. '
                            '(res_type and tenant_id are supported for now)')
        parser.add_argument('-a', '--all-tenants', action='store_true',
                            help='Allows to get summary from all tenants '
                            '(admin only). Defaults to False.')
        return parser


class CliTotalGet(show.ShowOne):
    """(DEPRECATED) Get total reports."""
    def take_action(self, parsed_args):
        for arg in ['begin', 'end']:
            value = getattr(parsed_args, arg)
            if value is not None:
                try:
                    setattr(parsed_args, arg, utils.iso2dt(value))
                except ValueError:
                    raise exc.InvalidArgumentError(
                        'Invalid timestamp "{}"'.format(value))
        resp = utils.get_client_from_osc(self).report.get_total(
            **vars(parsed_args))
        return ('Total', ), (float(resp), )

    def get_parser(self, prog_name):
        parser = super(CliTotalGet, self).get_parser(prog_name)
        parser.add_argument('-t', '--tenant-id',
                            help='Tenant id.')
        parser.add_argument('-b', '--begin', type=str,
                            help='Begin timestamp.')
        parser.add_argument('-e', '--end', type=str,
                            help='End timestamp.')
        parser.add_argument('-s', '--service',
                            help='Service Type.')
        parser.add_argument('-g', '--groupby', nargs='+',
                            help='Fields to group by, space-separated. '
                            '(res_type and tenant_id are supported for now)')
        parser.add_argument('-a', '--all-tenants', action='store_true',
                            help='Allows to get summary from all tenants '
                            '(admin only). Defaults to False.')
        return parser


class CliTenantList(lister.Lister):
    """Get rated tenants for the given period.

    Begin defaults to the beginning of the current month and end defaults to
    the beginning of the next month.
    """
    def take_action(self, parsed_args):
        for arg in ['begin', 'end']:
            value = getattr(parsed_args, arg)
            if value is not None:
                try:
                    setattr(parsed_args, arg, utils.iso2dt(value))
                except ValueError:
                    raise exc.InvalidArgumentError(
                        'Invalid timestamp "{}"'.format(value))
        client = utils.get_client_from_osc(self)
        tenants = client.report.get_tenants(**vars(parsed_args))
        output = []
        for tenant in tenants:
            output.append((tenant, ))
        return (('Tenant ID', ), output)

    def get_parser(self, prog_name):
        parser = super(CliTenantList, self).get_parser(prog_name)
        parser.add_argument('-b', '--begin', type=str,
                            help='Begin timestamp.')
        parser.add_argument('-e', '--end', type=str,
                            help='End timestamp.')
        return parser
