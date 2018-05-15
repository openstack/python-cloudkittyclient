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
from cliff import command
from cliff import lister

from cloudkittyclient import utils


class CliCollectorMappingGet(lister.Lister):
    """(DEPRECATED) Get a service to collector mapping."""

    columns = [
        ('service', 'Service'),
        ('collector', 'Collector'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).collector.get_mapping(
            service=parsed_args.service,
        )
        resp = [resp] if resp.get('mappings') is None else resp['mappings']
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingGet, self).get_parser(prog_name)
        parser.add_argument('service', type=str,
                            help='Name of the service to filter on')
        return parser


class CliCollectorMappingList(lister.Lister):
    """(DEPRECATED) List service to collector mappings."""

    columns = [
        ('service', 'Service'),
        ('collector', 'Collector'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).collector.get_mapping(
            collector=parsed_args.collector)
        resp = [resp] if resp.get('mappings') is None else resp['mappings']
        values = utils.list_to_cols(resp, self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingList, self).get_parser(prog_name)
        parser.add_argument('--collector', type=str,
                            help='Name of the collector to filter on')
        return parser


class CliCollectorMappingCreate(lister.Lister):
    """(DEPRECATED) Create a service to collector mapping."""

    columns = [
        ('service', 'Service'),
        ('collector', 'Collector'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).collector.create_mapping(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingCreate, self).get_parser(prog_name)
        parser.add_argument('service', type=str, help='Name of the service')
        parser.add_argument('collector', type=str,
                            help='Name of the collector')
        return parser


class CliCollectorMappingDelete(command.Command):
    """(DEPRECATED) Delete a service to collector mapping."""

    def take_action(self, parsed_args):
        utils.get_client_from_osc(self).collector.delete_mapping(
            **vars(parsed_args))

    def get_parser(self, prog_name):
        parser = super(CliCollectorMappingDelete, self).get_parser(prog_name)
        parser.add_argument('service', type=str, help='Name of the service')
        return parser


class CliCollectorGetState(lister.Lister):
    """(DEPRECATED) Get the state of a collector."""

    columns = [
        ('name', 'Collector'),
        ('enabled', 'State'),
    ]

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).collector.get_state(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCollectorGetState, self).get_parser(prog_name)
        parser.add_argument('name', type=str, help='Name of the collector')
        return parser


class CliCollectorEnable(lister.Lister):
    """(DEPRECATED) Enable a collector."""

    columns = [
        ('name', 'Collector'),
        ('enabled', 'State'),
    ]

    def take_action(self, parsed_args):
        parsed_args.enabled = True
        resp = utils.get_client_from_osc(self).collector.set_state(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values

    def get_parser(self, prog_name):
        parser = super(CliCollectorEnable, self).get_parser(prog_name)
        parser.add_argument('name', type=str, help='Name of the collector')
        return parser


class CliCollectorDisable(CliCollectorEnable):
    """(DEPRECATED) Disable a collector."""

    def take_action(self, parsed_args):
        parsed_args.disabled = True
        resp = utils.get_client_from_osc(self).collector.set_state(
            **vars(parsed_args))
        values = utils.list_to_cols([resp], self.columns)
        return [col[1] for col in self.columns], values
