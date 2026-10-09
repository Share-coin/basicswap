# -*- coding: utf-8 -*-

# Copyright (c) 2026 The Basicswap developers
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from basicswap.util import COIN

params = {
    "name": "sharecoin",
    "ticker": "SHC",
    "message_magic": "Sharecoin Signed Message:\n",
    "blocks_target": 120,
    "decimal_places": 8,
    "mainnet": {
        "rpcport": 8332,
        "pubkey_address": 63,
        "script_address": 18,
        "key_prefix": 214,
        "hrp": "shc",
        "ext_public_key_prefix": 0x042C03E3,
        "ext_secret_key_prefix": 0x042C081E,
        # Not registered in SLIP-44 yet, this index is unassigned there.
        "bip44": 8443,
        "min_amount": 100000,
        "max_amount": 10000000 * COIN,
    },
    "testnet": {
        "rpcport": 18332,
        "pubkey_address": 111,
        "script_address": 196,
        "key_prefix": 239,
        "hrp": "tshc",
        "ext_public_key_prefix": 0x043587CF,
        "ext_secret_key_prefix": 0x04358394,
        "bip44": 1,
        "min_amount": 100000,
        "max_amount": 10000000 * COIN,
        "name": "testnet3",
    },
    "regtest": {
        "rpcport": 18443,
        "pubkey_address": 111,
        "script_address": 196,
        "key_prefix": 239,
        "hrp": "shcrt",
        "ext_public_key_prefix": 0x043587CF,
        "ext_secret_key_prefix": 0x04358394,
        "bip44": 1,
        "min_amount": 100000,
        "max_amount": 10000000 * COIN,
        "name": "sharenet",
    },
}
