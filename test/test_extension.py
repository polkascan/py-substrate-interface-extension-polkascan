#  Polkascan API extension for Substrate Interface Library
#
#  Copyright 2018-2023 Stichting Polkascan (Polkascan Foundation).
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import unittest
from os import environ

from substrateinterface import SubstrateInterface
from substrateinterface_polkascan.extensions import PolkascanExtension

POLKADOT_NODE_URL = environ.get('SUBSTRATE_NODE_URL_POLKADOT') or 'ws://127.0.0.1:9944'
POLKASCAN_API_URL = environ.get('POLKASCAN_API_URL') or 'http://127.0.0.1:8000/graphql/'


class TestExtension(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.substrate = SubstrateInterface(url=POLKADOT_NODE_URL)
        cls.substrate.register_extension(PolkascanExtension(url=POLKASCAN_API_URL))

    def test_filter_events(self):

        events = self.substrate.extensions.filter_events(pallet_name="Balances", event_name="Transfer", page_size=5)

        self.assertEqual(len(events), 5)

    def test_filter_extrinsics(self):

        extrinsics = self.substrate.extensions.filter_extrinsics(
            ss58_address="12L9MSmxHY8YvtZKpA7Vpvac2pwf4wrT3gd2Tx78sCctoXSE",
            pallet_name="Balances", call_name="transfer_keep_alive", page_size=5
        )

        self.assertGreater(len(extrinsics), 0)


if __name__ == '__main__':
    unittest.main()
