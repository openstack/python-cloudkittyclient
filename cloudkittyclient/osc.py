# Copyright 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from osc_lib import utils

DEFAULT_API_VERSION = '1'
API_VERSION_OPTION = 'os_rating_api_version'
API_NAME = "rating"
API_VERSIONS = {
    "1": "cloudkittyclient.v1.client.Client",
    "2": "cloudkittyclient.v2.client.Client",
}


def make_client(instance):
    """Returns a rating service client."""
    version = instance._api_version[API_NAME]
    ck_client = utils.get_client_class(
        API_NAME,
        version,
        API_VERSIONS)
    instance.setup_auth()
    adapter_options = dict(
        interface=instance.interface,
        region_name=instance.region_name,
    )
    return ck_client(session=instance.session,
                     adapter_options=adapter_options)


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--rating-api-version', type=int, default=utils.env(
            'OS_RATING_API_VERSION',
            default=DEFAULT_API_VERSION)
    )
    return parser
