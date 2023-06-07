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

from substrateinterface.extensions import SearchExtension
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class PolkascanExtension(SearchExtension):

    def __init__(self, url: str):
        self.url = url
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url=url)

        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        super().__init__()

    def filter_events(self, block_start: int = None, block_end: int = None, pallet_name: str = None,
                      event_name: str = None, page_size: int = 10, page_number: int = 1) -> list:

        if block_start or block_end:
            raise NotImplementedError("Block range not supported by this extension")

        # Compose GraphQL query
        filters = []
        if pallet_name:
            filters.append('eventModule: "' + pallet_name + '"')
        if event_name:
            filters.append('eventName: "' + event_name + '"')

        query = gql('query { getEvents(filters: {' + ', '.join(filters) + '}, pageKey: "' + str(page_number) + '", pageSize: ' + str(page_size) + ') { objects { blockNumber, extrinsicIdx, eventIdx } } }')
        result = self.client.execute(query)
        events = []
        for item in result['getEvents']['objects']:
            # Retrieve actual events on-chain
            result = self.substrate.get_events(block_hash=self.substrate.get_block_hash(item['blockNumber']))
            events.append(result[item['eventIdx']])
        return events

    def filter_extrinsics(self, block_start: int = None, block_end: int = None, ss58_address: str = None,
                          pallet_name: str = None, call_name: str = None, page_size: int = 10, page_number: int = 1) -> list:

        if block_start or block_end:
            raise NotImplementedError("Block range not supported by this extension")

        # Compose GraphQL query
        filters = []
        if pallet_name:
            filters.append('callModule: "' + pallet_name + '"')
        if call_name:
            filters.append('callName: "' + call_name + '"')
        if ss58_address:
            filters.append('multiAddressAccountId: "0x' + self.substrate.ss58_decode(ss58_address) + '"')

        query = gql(
            'query { getExtrinsics(filters: {' + ', '.join(filters) + '}, pageKey: "' + str(
                page_number) + '", pageSize: ' + str(page_size) + ') { objects { blockNumber, extrinsicIdx } } }')

        result = self.client.execute(query)
        extrinsics = []
        for item in result['getExtrinsics']['objects']:
            # Retrieve actual extrinsics on-chain
            extrinsics.append(
                self.substrate.retrieve_extrinsic_by_identifier(f"{item['blockNumber']}-{item['extrinsicIdx']}")
            )
        return extrinsics
