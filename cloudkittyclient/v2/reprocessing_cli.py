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
from oslo_utils import timeutils

from cloudkittyclient import utils


class CliReprocessingTasksGet(lister.Lister):
    """Get reprocessing tasks."""

    result_columns = [
        ('scope_id', 'Scope ID'),
        ('reason', 'Reason'),
        ('start_reprocess_time', 'Start reprocessing time'),
        ('end_reprocess_time', 'End reprocessing time'),
        ('current_reprocess_time', 'Current reprocessing time'),
    ]

    def get_parser(self, prog_name):
        parser = super(CliReprocessingTasksGet, self).get_parser(prog_name)

        parser.add_argument('--scope-id', type=str, default=[],
                            action='append', help='Optional filter on scope '
                                                  'IDs. This filter can be '
                                                  'used multiple times.')

        parser.add_argument('--offset', type=int, default=0,
                            help='Index of the first scope. '
                                 'The default value is 0.')
        parser.add_argument('--limit', type=int, default=100,
                            help='Maximal number of scopes. '
                                 'The default value is 100.')
        parser.add_argument('--order', type=str, default="DESC",
                            help='The order to sort the reprocessing tasks '
                                 '(ASC or DESC).')

        return parser

    def take_action(self, parsed_args):
        resp = utils.get_client_from_osc(
            self).reprocessing.get_reprocessing_tasks(
            scope_ids=parsed_args.scope_id, offset=parsed_args.offset,
            limit=parsed_args.limit, order=parsed_args.order
        )

        values = utils.list_to_cols(resp['results'], self.result_columns)
        return [col[1] for col in self.result_columns], values


class CliReprocessingTasksPost(lister.Lister):
    """Create a reprocessing task."""

    def get_parser(self, prog_name):
        parser = super(CliReprocessingTasksPost, self).get_parser(prog_name)

        parser.add_argument('--scope-id', type=str, default=[],
                            action='append',
                            help='The scope IDs to reprocess. This option can '
                                 'be used multiple times to execute the same '
                                 'reprocessing task for different scope IDs.')

        parser.add_argument('--start-reprocess-time',
                            type=timeutils.parse_isotime,
                            help="Start of the period to reprocess in ISO8601 "
                                 "format. Example: '2022-04-22T00:00:00Z.'")

        parser.add_argument('--end-reprocess-time',
                            type=timeutils.parse_isotime,
                            help="End of the period to reprocess in ISO8601 "
                                 "format. Example: '2022-04-22T00:00:00Z.'")

        parser.add_argument('--reason', type=str,
                            help="The reason to create the reprocessing task.")

        return parser

    def take_action(self, parsed_args):
        return ["Result"], utils.get_client_from_osc(
            self).reprocessing.post_reprocessing_task(
            scope_ids=parsed_args.scope_id,
            start=parsed_args.start_reprocess_time,
            end=parsed_args.end_reprocess_time,
            reason=parsed_args.reason
        )
