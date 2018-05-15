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

from cloudkittyclient import exc
from cloudkittyclient import utils


class CliGetDataframes(lister.Lister):
    """List stored dataframes or generate CSV reports.

    Dataframes can be filtered on resource_type and project_id.
    CSV reports can be generated with the 'df-to-csv' formatter.
    A config file may be provided to configure the output of that formatter.
    See documentation for more details.
    """
    columns = [
        ('begin', 'Begin'),
        ('end', 'End'),
        ('tenant_id', 'Project ID'),
        ('resources', 'Resources'),
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
        resp = utils.get_client_from_osc(self).storage.get_dataframes(
            **vars(parsed_args)).get('dataframes', [])
        values = utils.list_to_cols(resp, self.columns)
        for value in values:
            for resource in value[3]:
                rating = float(resource['rating'])
                volume = float(resource['volume'])
                if volume > 0:
                    resource['rate_value'] = '{:.4f}'.format(rating / volume)
                else:
                    resource['rate_value'] = ''
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliGetDataframes, self).get_parser(prog_name)
        parser.add_argument('-b', '--begin', type=str, help='Begin timestamp')
        parser.add_argument('-e', '--end', type=str, help='End timestamp')
        parser.add_argument('-p', '--project-id', type=str, dest='tenant_id',
                            help='Id of the tenant to filter on')
        parser.add_argument('-r', '--resource_type', type=str,
                            help='Resource type to filter on')
        return parser
