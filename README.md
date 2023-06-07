# Python Substrate Interface: Polkascan Extension

[![Latest Version](https://img.shields.io/pypi/v/substrate-interface-polkascan.svg)](https://pypi.org/project/substrate-interface-polkascan/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/substrate-interface-polkascan.svg)](https://pypi.org/project/substrate-interface/)
[![License](https://img.shields.io/pypi/l/substrate-interface-polkascan.svg)](https://github.com/polkascan/py-substrate-interface-extension-polkascan/blob/master/LICENSE)


## Description
This extension enables [Substrate Interface](https://github.com/polkascan/py-substrate-interface) to use indexes provided by the [Polkascan Explorer API](https://github.com/polkascan/explorer#explorer-api-component)   

## Installation
```bash
pip install substrate-interface-polkascan
```

## Initialization

```python
from substrateinterface import SubstrateInterface
from substrateinterface_polkascan.extensions import PolkascanExtension

substrate = SubstrateInterface(url="ws://127.0.0.1:9944")

substrate.register_extension(PolkascanExtension(url='http://127.0.0.1:8000/graphql/'))
```

## Usage

### Filter events

```python
events = substrate.extensions.filter_events(pallet_name="Balances", event_name="Transfer", page_size=25)
```

### Filter extrinsics

```python
extrinsics = substrate.extensions.filter_extrinsics(
    ss58_address="12L9MSmxHY8YvtZKpA7Vpvac2pwf4wrT3gd2Tx78sCctoXSE",
    pallet_name="Balances", call_name="transfer_keep_alive", page_size=25
)
```

## License
https://github.com/polkascan/py-substrate-interface-extension-polkascan/blob/master/LICENSE
