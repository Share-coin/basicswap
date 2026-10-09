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

    def getWalletInfo(self):
        rv = super().getWalletInfo()
        if "balance" not in rv:
            # Balances were removed from getwalletinfo in the v31 base.
            balances = self.rpc_wallet("getbalances")["mine"]
            rv["balance"] = balances["trusted"]
            rv["unconfirmed_balance"] = balances["untrusted_pending"]
            rv["immature_balance"] = balances["immature"]
        return rv
