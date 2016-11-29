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

from cloudkittyclient.apiclient import exceptions
from cloudkittyclient.common import utils
from cloudkittyclient import exc

_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


@utils.arg('-n', '--name',
           help='Service name',
           required=True)
def do_hashmap_service_create(cc, args={}):
    """Create a service."""
    arg_to_field_mapping = {
        'name': 'name'
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap.services.create(**fields)
    utils.print_dict(out.to_dict())


def do_hashmap_service_list(cc, args={}):
    """List services."""
    try:
        services = cc.hashmap.services.list()
    except exceptions.NotFound:
        raise exc.CommandError('Services not found.')
    else:
        field_labels = ['Name', 'Service id']
        fields = ['name', 'service_id']
        utils.print_list(services, fields, field_labels,
                         sortby=0)


@utils.arg('-s', '--service-id',
           help='Service uuid',
           required=True)
def do_hashmap_service_delete(cc, args={}):
    """Delete a service."""
    try:
        cc.hashmap.services.delete(service_id=args.service_id)
    except exceptions.NotFound:
        raise exc.CommandError('Service not found: %s' % args.service_id)


@utils.arg('-n', '--name',
           help='Field name',
           required=True)
@utils.arg('-s', '--service-id',
           help='Service id',
           required=True)
def do_hashmap_field_create(cc, args={}):
    """Create a field."""
    arg_to_field_mapping = {
        'name': 'name',
        'service_id': 'service_id'
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap.fields.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-s', '--service-id',
           help='Service id',
           required=True)
def do_hashmap_field_list(cc, args={}):
    """List fields."""
    try:
        created_field = cc.hashmap.fields.list(service_id=args.service_id)
    except exceptions.NotFound:
        raise exc.CommandError('Fields not found in service: %s'
                               % args.service_id)
    else:
        field_labels = ['Name', 'Field id']
        fields = ['name', 'field_id']
        utils.print_list(created_field, fields, field_labels,
                         sortby=0)


@utils.arg('-f', '--field-id',
           help='Field uuid',
           required=True)
def do_hashmap_field_delete(cc, args={}):
    """Delete a field."""
    try:
        cc.hashmap.fields.delete(field_id=args.field_id)
    except exceptions.NotFound:
        raise exc.CommandError('Field not found: %s' % args.field_id)


def common_hashmap_mapping_arguments(create=False):
    def _wrapper(func):
        @utils.arg('-c', '--cost',
                   help='Mapping cost',
                   required=create)
        @utils.arg('-v', '--value',
                   help='Mapping value',
                   required=False)
        @utils.arg('-t', '--type',
                   help='Mapping type (flat, rate)',
                   required=False)
        @utils.arg('-g', '--group-id',
                   help='Group id',
                   required=False)
        @utils.arg('-p', '--project-id',
                   help='Project/tenant id',
                   required=False)
        @functools.wraps(func)
        def _wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        return _wrapped
    return _wrapper


@utils.arg('-s', '--service-id',
           help='Service id',
           required=False)
@utils.arg('-f', '--field-id',
           help='Field id',
           required=False)
@common_hashmap_mapping_arguments(create=True)
def do_hashmap_mapping_create(cc, args={}):
    """Create a mapping."""
    arg_to_field_mapping = {
        'cost': 'cost',
        'value': 'value',
        'type': 'type',
        'service_id': 'service_id',
        'field_id': 'field_id',
        'group_id': 'group_id',
        'project_id': 'tenant_id',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap.mappings.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-m', '--mapping-id',
           help='Mapping id',
           required=True)
@common_hashmap_mapping_arguments()
def do_hashmap_mapping_update(cc, args={}):
    """Update a mapping."""
    arg_to_field_mapping = {
        'mapping_id': 'mapping_id',
        'cost': 'cost',
        'value': 'value',
        'type': 'type',
        'group_id': 'group_id',
        'project_id': 'tenant_id',
    }
    try:
        mapping = cc.hashmap.mappings.get(mapping_id=args.mapping_id)
    except exceptions.NotFound:
        raise exc.CommandError('Mapping not found: %s' % args.mapping_id)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                setattr(mapping, k, v)
    cc.hashmap.mappings.update(**mapping.dirty_fields)


@utils.arg('-s', '--service-id',
           help='Service id',
           required=False)
@utils.arg('-f', '--field-id',
           help='Field id',
           required=False)
@utils.arg('-g', '--group-id',
           help='Group id',
           required=False)
@utils.arg('-p', '--project-id',
           help='Project/tenant id',
           required=False)
def do_hashmap_mapping_list(cc, args={}):
    """List mappings."""
    if (args.group_id is None and
       args.service_id is None and args.field_id is None):
        raise exc.CommandError("Provide either group-id, service-id or "
                               "field-id")
    try:
        mappings = cc.hashmap.mappings.list(service_id=args.service_id,
                                            field_id=args.field_id,
                                            group_id=args.group_id)
    except exceptions.NotFound:
        raise exc.CommandError('Mappings not found for field: %s'
                               % args.field_id)
    else:
        field_labels = ['Mapping id', 'Value', 'Cost',
                        'Type', 'Field id',
                        'Service id', 'Group id', 'Tenant id']
        fields = ['mapping_id', 'value', 'cost',
                  'type', 'field_id',
                  'service_id', 'group_id', 'tenant_id']
        utils.print_list(mappings, fields, field_labels,
                         sortby=0)


@utils.arg('-m', '--mapping-id',
           help='Mapping uuid',
           required=True)
def do_hashmap_mapping_delete(cc, args={}):
    """Delete a mapping."""
    try:
        cc.hashmap.mappings.delete(mapping_id=args.mapping_id)
    except exceptions.NotFound:
        raise exc.CommandError('Mapping not found: %s' % args.mapping_id)


@utils.arg('-n', '--name',
           help='Group name',
           required=True)
def do_hashmap_group_create(cc, args={}):
    """Create a group."""
    arg_to_field_mapping = {
        'name': 'name',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    group = cc.hashmap.groups.create(**fields)
    utils.print_dict(group.to_dict())


def do_hashmap_group_list(cc, args={}):
    """List groups."""
    try:
        groups = cc.hashmap.groups.list()
    except exceptions.NotFound:
        raise exc.CommandError('Groups not found.')
    else:
        field_labels = ['Name',
                        'Group id']
        fields = ['name', 'group_id']
        utils.print_list(groups, fields, field_labels,
                         sortby=0)


@utils.arg('-g', '--group-id',
           help='Group uuid',
           required=True)
@utils.arg('-r', '--recursive',
           help="""Delete the group's mappings""",
           required=False,
           default=False)
def do_hashmap_group_delete(cc, args={}):
    """Delete a group."""
    try:
        cc.hashmap.groups.delete(group_id=args.group_id,
                                 recursive=args.recursive)
    except exceptions.NotFound:
        raise exc.CommandError('Group not found: %s' % args.group_id)


def common_hashmap_threshold_arguments(create=False):
    def _wrapper(func):
        @utils.arg('-l', '--level',
                   help='Threshold level',
                   required=create)
        @utils.arg('-c', '--cost',
                   help='Threshold cost',
                   required=create)
        @utils.arg('-t', '--type',
                   help='Threshold type (flat, rate)',
                   required=False)
        @utils.arg('-g', '--group-id',
                   help='Group id',
                   required=False)
        @utils.arg('-p', '--project-id',
                   help='Project/tenant id',
                   required=False)
        @functools.wraps(func)
        def _wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        return _wrapped
    return _wrapper


@utils.arg('-s', '--service-id',
           help='Service id',
           required=False)
@utils.arg('-f', '--field-id',
           help='Field id',
           required=False)
@common_hashmap_threshold_arguments(create=True)
def do_hashmap_threshold_create(cc, args={}):
    """Create a mapping."""
    arg_to_field_mapping = {
        'level': 'level',
        'cost': 'cost',
        'type': 'type',
        'service_id': 'service_id',
        'field_id': 'field_id',
        'group_id': 'group_id',
        'project_id': 'tenant_id',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap.thresholds.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-i', '--threshold-id',
           help='Threshold id',
           required=True)
@common_hashmap_threshold_arguments()
def do_hashmap_threshold_update(cc, args={}):
    """Update a threshold."""
    arg_to_field_mapping = {
        'threshold_id': 'threshold_id',
        'cost': 'cost',
        'level': 'level',
        'type': 'type',
        'group_id': 'group_id',
        'project_id': 'tenant_id',
    }
    try:
        threshold = cc.hashmap.thresholds.get(threshold_id=args.threshold_id)
    except exceptions.NotFound:
        raise exc.CommandError('Threshold not found: %s' % args.threshold_id)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                setattr(threshold, k, v)
    cc.hashmap.thresholds.update(**threshold.dirty_fields)


@utils.arg('-s', '--service-id',
           help='Service id',
           required=False)
@utils.arg('-f', '--field-id',
           help='Field id',
           required=False)
@utils.arg('-g', '--group-id',
           help='Group id',
           required=False)
@utils.arg('--no-group',
           type=_bool_strict, metavar='{True,False}',
           help='If True, list only orhpaned thresholds',
           required=False)
@utils.arg('-p', '--project-id',
           help='Project/tenant id',
           required=False)
def do_hashmap_threshold_list(cc, args={}):
    """List thresholds."""
    if (args.group_id is None and
       args.service_id is None and args.field_id is None):
        raise exc.CommandError("Provide either group-id, service-id or "
                               "field-id")
    try:
        thresholds = cc.hashmap.thresholds.list(service_id=args.service_id,
                                                field_id=args.field_id,
                                                group_id=args.group_id,
                                                no_group=args.no_group)
    except exceptions.NotFound:
        raise exc.CommandError('Thresholds not found')
    else:
        field_labels = ['Threshold id', 'Level', 'Cost',
                        'Type', 'Field id',
                        'Service id', 'Group id', 'Tenant id']
        fields = ['threshold_id', 'level', 'cost',
                  'type', 'field_id',
                  'service_id', 'group_id', 'tenant_id']
        utils.print_list(thresholds, fields, field_labels, sortby=0)


@utils.arg('-i', '--threshold-id',
           help='Threshold uuid',
           required=True)
def do_hashmap_threshold_delete(cc, args={}):
    """Delete a threshold."""
    try:
        cc.hashmap.thresholds.delete(threshold_id=args.threshold_id)
    except exceptions.NotFound:
        raise exc.CommandError('Threshold not found: %s' % args.threshold_id)


@utils.arg('-i', '--threshold-id',
           help='Threshold uuid',
           required=True)
def do_hashmap_threshold_get(cc, args={}):
    """Get a threshold."""
    try:
        threshold = cc.hashmap.thresholds.get(threshold_id=args.threshold_id)
    except exceptions.NotFound:
        raise exc.CommandError('Threshold not found: %s' % args.threshold_id)
    utils.print_dict(threshold.to_dict())


@utils.arg('-i', '--threshold-id',
           help='Threshold uuid',
           required=True)
def do_hashmap_threshold_group(cc, args={}):
    """Get a threshold group."""
    try:
        threshold = cc.hashmap.thresholds.group(threshold_id=args.threshold_id)
    except exceptions.NotFound:
        raise exc.CommandError('Threshold not found: %s' % args.threshold_id)
    utils.print_dict(threshold.to_dict())
