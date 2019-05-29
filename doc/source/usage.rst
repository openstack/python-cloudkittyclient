=====
Usage
=====

CLI
===

Authentication
--------------

The CloudKitty client can either be used through the standalone CLI executable
(``cloudkitty``) or through the OpenStack Client module (``openstack rating``).

When using CloudKitty in standalone mode (ie without Keystone authentication),
the API endpoint and the auth method must be specified:

.. code-block:: shell

   cloudkitty --os-endpoint http://cloudkitty-api:8889 --os-auth-type cloudkitty-noauth module list

These options can also be specified as environment variables:

.. code-block:: shell

   export OS_ENDPOINT=http://cloudkitty-api:8889
   export OS_AUTH_TYPE=cloudkitty-noauth
   cloudkitty module list

The exact same options apply when using the OpenStack Client plugin:

.. code-block:: shell

   # EITHER
   openstack rating --os-endpoint http://cloudkitty-api:8889 --os-auth-type cloudkitty-noauth module list

   # OR
   export OS_ENDPOINT=http://cloudkitty-api:8889
   export OS_AUTH_TYPE=cloudkitty-noauth
   openstack rating module list

Version
-------

Two versions of the client exist: v1 and v2. The v2 version adds support for
v2 API endpoints. The default API version is 1. You can specify which API
version you want to use via a CLI option:

.. code-block:: shell

   # EITHER
   cloudkitty --os-rating-api-version 2 summary get

   # OR
   export OS_RATING_API_VERSION=2
   cloudkitty summary get

Again, the option can also be provided to the OSC plugin, both via the CLI
flag or the environment variable.

Python library
==============

You can use cloudkittyclient with or without keystone authentication. In order
to use it without keystone authentication, cloudkittyclient provides the
``CloudKittyNoAuthPlugin`` keystoneauth plugin::

    >>> from cloudkittyclient import client as ck_client
    >>> from cloudkittyclient import auth as ck_auth

    >>> auth = ck_auth.CloudKittyNoAuthPlugin(endpoint='http://127.0.0.1:8889')
    >>> client = ck_client.Client('1', auth=auth)
    >>> client.report.get_summary()
    {u'summary': [{u'begin': u'2018-03-01T00:00:00',
                   u'end': u'2018-04-01T00:00:00',
                   u'rate': u'1672.71269',
                   u'res_type': u'ALL',
                   u'tenant_id': u'bea6a24f77e946b0a92dca7c78b7870b'}]}

Else, use it the same way as any other OpenStack client::

   >>> import os

   >>> from keystoneauth1 import session
   >>> from keystoneauth1.identity import v3

   >>> from cloudkittyclient import client as ck_client

   >>> auth = v3.Password(
          auth_url=os.environ.get('OS_AUTH_URL'),
          project_domain_id=os.environ.get('OS_PROJECT_DOMAIN_ID'),
          user_domain_id=os.environ.get('OS_USER_DOMAIN_ID'),
          username=os.environ.get('OS_USERNAME'),
          project_name=os.environ.get('OS_PROJECT_NAME'),
          password=os.environ.get('OS_PASSWORD'))

   >>> ck_session = session.Session(auth=auth)

   >>> c = ck_client.Client('1', session=ck_session)

   >>> c.report.get_summary()
   {u'summary': [{u'begin': u'2018-03-01T00:00:00',
                   u'end': u'2018-04-01T00:00:00',
                   u'rate': u'1672.71269',
                   u'res_type': u'ALL',
                   u'tenant_id': u'bea6a24f77e946b0a92dca7c78b7870b'}]}

.. warning::

   If you want to use SSL with the client as a python library, you need to
   provide a cert to keystone's session object. Else, two additional options
   are available if you provide an ``auth`` object to the client: ``insecure``
   and ``cacert``::

     >>> client = ck_client.Client(
             '1', auth=auth, insecure=False, cacert='/path/to/ca')


If you want to use the v2 API, you have to specify it at client instanciation

.. code-block:: python

   c = ck_client.Client('2', session=session)

When using the ``cloudkitty`` CLI client with keystone authentication, the
auth plugin to use should automagically be detected. If not, you can specify
the auth plugin to use with ``--os-auth-type/--os-auth-plugin``::

    $ cloudkitty --debug --os-auth-type cloudkitty-noauth summary get
    +------------+---------------+------------+---------------------+---------------------+
    | Project ID | Resource Type | Rate       | Begin Time          | End Time            |
    +------------+---------------+------------+---------------------+---------------------+
    | ALL        | ALL           | 1676.95499 | 2018-03-01T00:00:00 | 2018-04-01T00:00:00 |
    +------------+---------------+------------+---------------------+---------------------+


CSV report generation
=====================

An output formatter (``DataframeToCsvFormatter``) has been created in order to
allow CSV report generation through the client. It can be used with the
``-f df-to-csv`` option.

.. code:: shell

   $ cloudkitty dataframes get -b 2018-03-22T12:00:00 -f df-to-csv
   Begin,End,Metric Type,Qty,Cost,Project ID,Resource ID,User ID
   2018-03-01T12:00:00,2018-03-01T13:00:00,compute,1,2.0,53c3fe396a1a4ab0914b9aa997a5ff88,382d23c3-7b77-4e32-8d65-b3baf86ed7bb,38c1949c2e624f729b30e034ac787640
   [...]


.. warning:: The ``df-to-csv`` formatter should NEVER be used together with the
   ``-c/--column`` option and should only be used for the ``dataframes get``
   command.

The example above shows how to get a CSV report with the standard columns. If
you want other columns, it is possible to customize the formatter through a
configuration file:

.. literalinclude:: ../../etc/cloudkitty/csv_config.yml

Example with this config file::

    $ cloudkitty dataframes get -f df-to-csv --format-config-file /etc/cloudkitty/csv_config.yml > report.csv
    $ head -n 2 report.csv
    Begin,End,User ID,Resource ID,Qty,Cost
    2018-03-01T12:00:00,2018-03-01T13:00:00,38c1949c2e624f729b30e034ac787640,382d23c3-7b77-4e32-8d65-b3baf86ed7bb,1,2.0

An other config file is provided: ``legacy_csv_config.yml``. This file is
compatible with the format of ``cloudkitty-writer``'s CSV reports.
