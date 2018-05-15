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
import pbr.version

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
