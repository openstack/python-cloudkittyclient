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

from cloudkittyclient import utils


class CliInfoMetricGet(lister.Lister):
    """Get information about current metrics."""
    info_columns = [
        ('metric_id', 'Metric'),
        ('unit', 'Unit'),
        ('metadata', 'Metadata'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).info.get_metric(
            metric_name=parsed_args.metric_name,
        )
        values = utils.list_to_cols([resp], self.info_columns)
        return [col[1] for col in self.info_columns], values

    def get_parser(self, prog_name):
        parser = super(CliInfoMetricGet, self).get_parser(prog_name)
        parser.add_argument('metric_name',
                            type=str, default='', help='Metric name')
        return parser


class CliInfoMetricList(lister.Lister):
    """Get information about a single metric."""
    info_columns = [
        ('metric_id', 'Metric'),
        ('unit', 'Unit'),
        ('metadata', 'Metadata'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).info.get_metric()
        values = utils.list_to_cols(resp['metrics'], self.info_columns)
        return [col[1] for col in self.info_columns], values


class CliInfoConfigGet(lister.Lister):
    """Get information about the current configuration."""
    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).info.get_config()
        values = [(key, value) for key, value in resp.items()]
        return ('Section', 'Value'), values
