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
import json

from collections import OrderedDict

from cloudkittyclient import exc
from cloudkittyclient.tests.unit.v2 import base


class TestDataframes(base.BaseAPIEndpointTestCase):
    dataframes_data = """
    {
        "dataframes": [
            {
                "period": {
                    "begin": "20190723T122810Z",
                    "end": "20190723T132810Z"
                },
                "usage": {
                    "metric_one": [
                        {
                            "vol": {
                                "unit": "GiB",
                                "qty": 1.2
                            },
                            "rating": {
                                "price": 0.04
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ],
                    "metric_two": [
                        {
                            "vol": {
                                "unit": "MB",
                                "qty": 200.4
                            },
                            "rating": {
                                "price": 0.06
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ]
                }
            },
            {
                "period": {
                    "begin": "20190823T122810Z",
                    "end": "20190823T132810Z"
                },
                "usage": {
                    "metric_one": [
                        {
                            "vol": {
                                "unit": "GiB",
                                "qty": 2.4
                            },
                            "rating": {
                                "price": 0.08
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ],
                    "metric_two": [
                        {
                            "vol": {
                                "unit": "MB",
                                "qty": 400.8
                            },
                            "rating": {
                                "price": 0.12
                            },
                            "groupby": {
                                "group_one": "one",
                                "group_two": "two"
                            },
                            "metadata": {
                                "attr_one": "one",
                                "attr_two": "two"
                            }
                        }
                    ]
                }
            }
        ]
    }
    """

    def test_add_dataframes_with_string(self):
        self.dataframes.add_dataframes(
            dataframes=self.dataframes_data,
        )
        self.api_client.post.assert_called_once_with(
            '/v2/dataframes',
            data=self.dataframes_data,
        )

    def test_add_dataframes_with_json_object(self):
        json_data = json.loads(self.dataframes_data)

        self.dataframes.add_dataframes(
            dataframes=json_data,
        )
        self.api_client.post.assert_called_once_with(
            '/v2/dataframes',
            data=json.dumps(json_data),
        )

    def test_add_dataframes_with_neither_string_nor_object_raises_exc(self):
        self.assertRaises(
            exc.InvalidArgumentError,
            self.dataframes.add_dataframes,
            dataframes=[open],
        )

    def test_add_dataframes_with_no_args_raises_exc(self):
        self.assertRaises(
            exc.ArgumentRequired,
            self.dataframes.add_dataframes)

    def test_get_dataframes(self):
        self.dataframes.get_dataframes()
        self.api_client.get.assert_called_once_with('/v2/dataframes')

    def test_get_dataframes_with_pagination_args(self):
        self.dataframes.get_dataframes(offset=10, limit=10)
        try:
            self.api_client.get.assert_called_once_with(
                '/v2/dataframes?limit=10&offset=10')
        except AssertionError:
            self.api_client.get.assert_called_once_with(
                '/v2/dataframes?offset=10&limit=10')

    def test_get_dataframes_filters(self):
        self.dataframes.get_dataframes(
            filters=OrderedDict([('one', 'two'), ('three', 'four')]))
        self.api_client.get.assert_called_once_with(
            '/v2/dataframes?filters=one%3Atwo%2Cthree%3Afour')
