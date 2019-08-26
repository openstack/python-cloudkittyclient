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
import argparse

from cliff import command

from cloudkittyclient import utils


class CliDataframesAdd(command.Command):
    """Add one or several DataFrame objects to the storage backend."""
    def get_parser(self, prog_name):
        parser = super(CliDataframesAdd, self).get_parser(prog_name)

        parser.add_argument(
            'datafile',
            type=argparse.FileType('r'),
            help="File formatted as a JSON object having a DataFrame list"
                 "under a 'dataframes' key."
                 "'-' (hyphen) can be specified for using stdin.",
            )

        return parser

    def take_action(self, parsed_args):
        with parsed_args.datafile as dfile:
            dataframes = dfile.read()
            utils.get_client_from_osc(self).dataframes.add_dataframes(
                dataframes=dataframes,
            )
