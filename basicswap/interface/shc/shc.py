# -*- coding: utf-8 -*-

# Copyright (c) 2026 The Basicswap developers
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from basicswap.chainparams import Coins
from basicswap.interface.btc.btc import BTCInterface


class SHCInterface(BTCInterface):
    @staticmethod
    def coin_type():
        return Coins.SHC

    def max_money(self) -> int:
        return 500000000 * self.COIN()
