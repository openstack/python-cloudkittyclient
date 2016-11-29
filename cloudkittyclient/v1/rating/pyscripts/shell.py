# Copyright 2015 Objectif Libre
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
import functools

from oslo_utils import strutils
import six

from cloudkittyclient.apiclient import exceptions
from cloudkittyclient.common import utils
from cloudkittyclient import exc

_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


@utils.arg('-n', '--name',
           help='Script name',
           required=True)
@utils.arg('-f', '--file',
           help='Script file',
           required=False)
def do_pyscripts_script_create(cc, args={}):
    """Create a script."""
    script_args = {'name': args.name}
    if args.file:
        with open(args.file) as fp:
            script_args['data'] = fp.read()
    out = cc.pyscripts.scripts.create(**script_args)
    utils.print_dict(out.to_dict())


@utils.arg('-d', '--show-data',
           help='Show data in the listing',
           required=False,
           default=False)
def do_pyscripts_script_list(cc, args={}):
    """List scripts."""
    request_args = {}
    if not args.show_data:
        request_args['no_data'] = True
    scripts = cc.pyscripts.scripts.list(**request_args)
    field_labels = ['Name', 'Script id', 'Data', 'Checksum']
    fields = ['name', 'script_id', 'data', 'checksum']
    utils.print_list(scripts,
                     fields,
                     field_labels,
                     sortby=0)


@utils.arg('-s', '--script-id',
           help='Script uuid',
           required=True)
def do_pyscripts_script_get(cc, args={}):
    """Get script."""
    try:
        script = cc.pyscripts.scripts.get(script_id=args.script_id)
    except exceptions.NotFound:
        raise exc.CommandError('Script not found: %s' % args.script_id)
    utils.print_dict(script.to_dict())


@utils.arg('-s', '--script-id',
           help='Script uuid',
           required=True)
def do_pyscripts_script_get_data(cc, args={}):
    """Get script data."""
    try:
        script = cc.pyscripts.scripts.get(script_id=args.script_id)
    except exceptions.NotFound:
        raise exc.CommandError('Script not found: %s' % args.script_id)
    six.print_(script.data)


@utils.arg('-s', '--script-id',
           help='Script uuid',
           required=True)
def do_pyscripts_script_delete(cc, args={}):
    """Delete a script."""
    try:
        cc.pyscripts.scripts.delete(script_id=args.script_id)
    except exceptions.NotFound:
        raise exc.CommandError('Script not found: %s' % args.script_id)


@utils.arg('-s', '--script-id',
           help='Script uuid',
           required=True)
@utils.arg('-f', '--file',
           help='Script file',
           required=True)
def do_pyscripts_script_update(cc, args={}):
    """Update a mapping."""
    excluded_fields = [
        'checksum',
    ]
    with open(args.file) as fp:
        content = fp.read()
    try:
        script = cc.pyscripts.scripts.get(script_id=args.script_id)
    except exceptions.NotFound:
        raise exc.CommandError('Script not found: %s' % args.script_id)
    script_dict = script.to_dict()
    for field in excluded_fields:
        del script_dict[field]
    script_dict['data'] = content
    cc.pyscripts.scripts.update(**script_dict)
