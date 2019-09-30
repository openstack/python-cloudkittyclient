# Copyright 2019 Objectif Libre
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


class CliModuleList(lister.Lister):
    """Get loaded rating modules list"""

    def get_parser(self, prog_name):
        parser = super(CliModuleList, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(self).ratingmodules.get_modules_list()
        return resp['modules']
