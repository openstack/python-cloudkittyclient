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
import os
from sys import argv

import cliff.app
from cliff.commandmanager import CommandManager
import os_client_config
from oslo_log import log

from cloudkittyclient import client
from cloudkittyclient.osc import DEFAULT_API_VERSION
from cloudkittyclient import utils


LOG = log.getLogger(__name__)


class CloudKittyShell(cliff.app.App):

    legacy_commands = [
        'module-list',
        'module-enable',
        'module-list',
        'module-enable',
        'module-disable',
        'module-set-priority',
        'info-config-get',
        'info-service-get',
        'total-get',
        'summary-get',
        'report-tenant-list',
        'collector-mapping-list',
        'collector-mapping-get',
        'collector-mapping-create',
        'collector-mapping-delete',
        'collector-state-get',
        'collector-state-enable',
        'collector-state-disable',
        'storage-dataframe-list',
        'hashmap-service-create',
        'hashmap-service-list',
        'hashmap-service-delete',
        'hashmap-field-create',
        'hashmap-field-list',
        'hashmap-field-delete',
        'hashmap-mapping-create',
        'hashmap-mapping-update',
        'hashmap-mapping-list',
        'hashmap-mapping-delete',
        'hashmap-group-create',
        'hashmap-group-list',
        'hashmap-group-delete',
        'hashmap-threshold-create'
        'hashmap-threshold-update'
        'hashmap-threshold-list',
        'hashmap-threshold-delete',
        'hashmap-threshold-get',
        'hashmap-threshold-group',
        'pyscripts-script-create',
        'pyscripts-script-list',
        'pyscripts-script-get',
        'pyscripts-script-get-data',
        'pyscripts-script-delete',
        'pyscripts-script-update',
    ]

    def _get_api_version(self, args):
        # FIXME(peschk_l): This is a hacky way to figure out the client version
        # to load. If anybody has a better idea, please fix this.
        self.deferred_help = True
        parser = self.build_option_parser('CloudKitty CLI client',
                                          utils.get_version())
        del self.deferred_help
        parsed_args = parser.parse_known_args(args)
        return str(parsed_args[0].os_rating_api_version or DEFAULT_API_VERSION)

    def __init__(self, args):
        self._args = args
        self.cloud_config = os_client_config.OpenStackConfig()
        super(CloudKittyShell, self).__init__(
            description='CloudKitty CLI client',
            version=utils.get_version(),
            command_manager=CommandManager('cloudkittyclient_v{}'.format(
                self._get_api_version(args[:]),
            )),
            deferred_help=True,
        )
        self._client = None

    # NOTE(peschk_l): Used to warn users about command syntax change in Rocky.
    # To be deleted in S.
    def run_subcommand(self, argv):
        try:
            self.command_manager.find_command(argv)
        except ValueError:
            if argv[0] in self.legacy_commands:
                LOG.warning('WARNING: This command is deprecated, please see'
                            ' the reference for the new commands\n')
                exit(1)
        return super(CloudKittyShell, self).run_subcommand(argv)

    def build_option_parser(self, description, version):
        parser = super(CloudKittyShell, self).build_option_parser(
            description,
            version,
            argparse_kwargs={'allow_abbrev': False})
        if 'OS_AUTH_TYPE' not in os.environ.keys() \
           and 'OS_PASSWORD' in os.environ.keys():
            os.environ['OS_AUTH_TYPE'] = 'password'
        self.cloud_config.register_argparse_arguments(
            parser, self._args, service_keys=['rating'])
        return parser

    @property
    def client(self):
        if self._client is None:
            self.cloud = self.cloud_config.get_one_cloud(
                argparse=self.options)
            session = self.cloud.get_session()
            adapter_options = dict(
                service_type=(self.options.os_rating_service_type or
                              self.options.os_service_type),
                service_name=(self.options.os_rating_service_name or
                              self.options.os_service_name),
                interface=(self.options.os_rating_interface or
                           self.options.os_interface),
                region_name=self.options.os_region_name,
                endpoint_override=(
                    self.options.os_rating_endpoint_override or
                    self.options.os_endpoint_override),
            )
            self._client = client.Client(
                str(self.options.os_rating_api_version or DEFAULT_API_VERSION),
                session=session,
                adapter_options=adapter_options)
        return self._client


def main(args=None):
    if args is None:
        args = argv[1:]
    client_app = CloudKittyShell(args)
    return client_app.run(args)
