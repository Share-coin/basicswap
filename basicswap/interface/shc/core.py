# -*- coding: utf-8 -*-

# Copyright (c) 2026 The Basicswap developers
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

import os

from basicswap.interface.prepare_util import (
    CoinPrepareModule,
    PrepareContext,
    ensurePubkey,
)
from basicswap.interface.shc.chainparams import params

SHARECOIN_VERSION = os.getenv("SHARECOIN_VERSION", "1.0.0")
SHARECOIN_VERSION_TAG = os.getenv("SHARECOIN_VERSION_TAG", "")
# Single release-signing key, SHA256SUMS.asc is a clearsigned file.
sharecoin_signers = {"releases": ("86B410C06A18A1647557BB2B23AEF4BF0FB8E55E",)}

SHC_RPC_HOST = os.getenv("SHC_RPC_HOST", "127.0.0.1")
SHC_RPC_PORT = int(os.getenv("SHC_RPC_PORT", 8332))
SHC_ONION_PORT = int(os.getenv("SHC_ONION_PORT", 8443))
SHC_RPC_USER = os.getenv("SHC_RPC_USER", "")
SHC_RPC_PWD = os.getenv("SHC_RPC_PWD", "")


class SHCPrepare(CoinPrepareModule):
    def getConfigSegment(self, ctx: PrepareContext) -> dict:
        config = {
            "connection_type": "rpc",
            "manage_daemon": ctx.should_manage_daemon(self.ticker),
            "rpchost": SHC_RPC_HOST,
            "rpcport": SHC_RPC_PORT + ctx.port_offset,
            "onionport": SHC_ONION_PORT + ctx.port_offset,
            "datadir": os.getenv("SHC_DATA_DIR", os.path.join(ctx.data_dir, self.name)),
            "bindir": os.path.join(ctx.bin_dir, self.name),
            "use_segwit": True,
            "use_csv": True,
            # Low network hashrate makes short reorgs cheap.
            "blocks_confirmed": 20,
            "conf_target": 2,
            "core_version_no": self.version + self.version_tag,
            "core_version_group": 31,
            "min_relay_fee": 0.00001,
            # The v31 base can no longer create legacy wallets.
            "use_descriptors": True,
            "watch_wallet_name": "bsx_watch",
        }

        if self.rpc_user != "":
            config["rpcuser"] = self.rpc_user
            config["rpcpassword"] = self.rpc_password

        return config

    def hasDetachedSig(self) -> bool:
        return False

    def verifyCoreSignature(
        self,
        ctx: PrepareContext,
        gpg,
        release_path: str,
        assert_path: str,
        assert_sig_path: str,
        signing_key_name: str,
        extra_opts: dict,
    ) -> None:
        pubkey_filename = self.getPubkeyFilename(signing_key_name)
        pubkeyurls = self.getAllPubkeyUrls(ctx)

        ensurePubkey(
            gpg, ctx, signing_key_name, self.signers, pubkey_filename, pubkeyurls
        )

        with open(assert_path, "rb") as fp:
            verified = gpg.verify_file(fp)

        self.ensureValidSignatureBy(
            ctx, verified, signing_key_name, filepath=assert_path
        )

    def getExtractBins(self) -> list:
        return ["sharecoind", "sharecoin-cli"]

    def getExtractPath(
        self,
        ctx: PrepareContext,
        bin_name: str,
        release_path: str,
        extra_opts: dict,
    ) -> str:
        return f"sharecoin-linux-x64/{bin_name}"

    def getReleaseFilename(self, ctx: PrepareContext, arch_name: str) -> str:
        if ctx.bin_arch != "x86_64-linux-gnu":
            raise NotImplementedError("Sharecoin releases are linux x86_64 only.")
        return "sharecoin-linux-x64.tar.gz"

    def getReleaseUrl(self, ctx: PrepareContext, release_filename: str) -> str:
        return f"https://github.com/Share-coin/Sharecoin/releases/download/v{self.version}/{release_filename}"

    def getAssertUrl(
        self,
        ctx: PrepareContext,
        os_name: str,
        os_dir_name: str,
        signing_key_name: str,
        use_guix: bool,
    ) -> str:
        return f"https://github.com/Share-coin/Sharecoin/releases/download/v{self.version}/SHA256SUMS.asc"

    def writeCoinConfig(
        self,
        ctx: PrepareContext,
        fp,
        chain: str,
        salt: str,
        settings: dict,
        extra_opts: dict,
    ) -> None:
        fp.write("prune=4000\n")
        fp.write("changetype=bech32\n")
        fp.write("fallbackfee=0.0002\n")
        fp.write(f"pid={self.name}.pid\n")
        self.writeRpcAuth(fp, salt)

    def prepareDataDir(
        self,
        ctx: PrepareContext,
        settings: dict,
        chain: str,
        extra_opts: dict,
    ) -> None:
        super().prepareDataDir(ctx, settings, chain, extra_opts)
        if chain != "regtest":
            return
        # Sharecoin's regtest network is named sharenet.
        core_settings = settings["chainclients"][self.name]
        core_conf_name = core_settings.get("config_filename", self.name + ".conf")
        core_conf_path = os.path.join(core_settings["datadir"], core_conf_name)
        with open(core_conf_path) as fp:
            conf = fp.read()
        with open(core_conf_path, "w") as fp:
            fp.write(conf.replace("[regtest]\n", "[sharenet]\n"))


prepare_module = SHCPrepare(
    name=params["name"],
    ticker=params["ticker"],
    version=SHARECOIN_VERSION,
    version_tag=SHARECOIN_VERSION_TAG,
    signers=sharecoin_signers,
    rpc_user=SHC_RPC_USER,
    rpc_password=SHC_RPC_PWD,
    onion_port=SHC_ONION_PORT,
    creates_wallet=True,
)
