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

from cloudkittyclient.v1.storage import shell


class CliStorageDataframeList(command.Command):
    """List dataframes."""
    def get_parser(self, prog_name):
        parser = super(CliStorageDataframeList, self).get_parser(prog_name)
        parser.add_argument('-b', '--begin',
                            help='Starting date/time (YYYY-MM-ddThh:mm:ss)',
                            required=False)
        parser.add_argument('-e', '--end',
                            help='Ending date/time (YYYY-MM-ddThh:mm:ss)',
                            required=False)
        parser.add_argument('-t', '--tenant',
                            help='Tenant ID',
                            required=False,
                            default=None)
        parser.add_argument('-r', '--resource-type',
                            help='Resource type (compute, image...)',
                            required=False,
                            default=None)
        return parser

    def take_action(self, parsed_args):
        ckclient = self.app.client_manager.rating
        shell.do_storage_dataframe_list(ckclient, parsed_args)
