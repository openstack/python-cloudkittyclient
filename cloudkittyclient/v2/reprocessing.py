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
from cloudkittyclient.common import base
from cloudkittyclient import exc


class ReprocessingManager(base.BaseManager):
    """Class used to handle /v2/task/reprocesses endpoint"""

    url = '/v2/task/reprocesses'

    def get_reprocessing_tasks(self, offset=0, limit=100, scope_ids=[],
                               order="DESC", **kwargs):
        """Returns a paginated list of reprocessing tasks.

        Some optional filters can be provided.

        :param offset: Index of the first reprocessing task
        that should be returned.
        :type offset: int
        :param limit: Maximal number of reprocessing task to return.
        :type limit: int
        :param scope_ids: Optional scope_ids to filter on.
        :type scope_ids: list of str
        :param order: Optional order (asc/desc) to sort tasks.
        :type order: str
        """
        kwargs = kwargs or {}
        kwargs['order'] = order
        kwargs['offset'] = offset
        kwargs['limit'] = limit

        authorized_args = ['offset', 'limit', 'order']
        url = self.get_url(None, kwargs, authorized_args=authorized_args)

        if scope_ids:
            url += "&scope_ids=%s" % (",".join(scope_ids))
        return self.api_client.get(url).json()

    def post_reprocessing_task(self, scope_ids=[], start=None, end=None,
                               reason=None, **kwargs):
        """Creates a reprocessing task

        :param start: The start date of the reprocessing task
        :type start: timeutils.parse_isotime
        :param end: The end date of the reprocessing task
        :type end: timeutils.parse_isotime
        :param scope_ids: The scope IDs to create the reprocessing task to
        :type scope_ids: list of str
        :param reason: The reason for the reprocessing task
        :type reason: str
        """

        if not scope_ids:
            raise exc.ArgumentRequired("'scope-id' argument is required")

        body = dict(
            scope_ids=scope_ids,
            start_reprocess_time=start,
            end_reprocess_time=end,
            reason=reason
        )

        body = dict(filter(lambda elem: bool(elem[1]), body.items()))

        return self.api_client.post(self.url, json=body).json()
