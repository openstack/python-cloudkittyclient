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
import inspect

import pbr.version

from keystoneauth1.exceptions import http
from oslo_utils import timeutils


def get_version():
    """Returns cloudkittyclient's version."""
    return pbr.version.VersionInfo('python-cloudkittyclient').version_string()


def iso2dt(iso_date):
    """iso8601 format to datetime."""
    iso_dt = timeutils.parse_isotime(iso_date)
    trans_dt = timeutils.normalize_time(iso_dt)
    return trans_dt


def get_client_from_osc(obj):
    if hasattr(obj.app, 'client_manager'):
        return obj.app.client_manager.rating
    return obj.app.client


def dict_to_cols(dict_obj, cols):
    """Converts a dict to a cliff-compatible value list.

    For cliff lister.Lister objects, you should use list_to_cols() instead
    of this function.
    'cols' shouls be a list of (key, Name) tuples.
    """
    values = []
    for col in cols:
        values.append(dict_obj.get(col[0]))
    return values


def list_to_cols(list_obj, cols):
    if not isinstance(list_obj, list):
        list_obj = [list_obj]
    values = []
    for item in list_obj:
        values.append(dict_to_cols(item, cols))
    return values


def http_error_formatter(func):
    """This decorator catches Http Errors and re-formats them"""

    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except http.HttpError as e:
            raise http.HttpError(message=e.response.text,
                                 http_status=e.http_status)

    return wrap


def format_http_errors(ignore):
    """Applies ``http_error_formatter`` to all methods of a class.

    :param ignore: List of function names to ignore
    :type ignore: iterable
    """

    def wrap(cls):
        def predicate(item):
            # This avoids decorating functions of parent classes
            return (inspect.isfunction(item)
                    and item.__name__ not in ignore
                    and not item.__name__.startswith('_')
                    and cls.__name__ in item.__qualname__)

        for name, func in inspect.getmembers(cls, predicate):
            setattr(cls, name, http_error_formatter(func))

        return cls

    return wrap
