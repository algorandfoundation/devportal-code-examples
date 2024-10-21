import base64
from hashlib import sha256

import algokit_utils
import pytest
from algokit_utils import (
    Account,
    get_localnet_default_account,
    is_localnet,
)
from algosdk.transaction import (
    LogicSig,
    LogicSigTransaction,
    PaymentTxn,
    wait_for_confirmation,
)
from algosdk.v2client.algod import AlgodClient


@pytest.fixture(scope="session")
def lsig_template() -> str:
    with open("./smart_contracts/artifacts/self_payment/self_payment.teal") as f:
        return f.read()


@pytest.fixture(scope="session")
def delegating_account(algod_client: AlgodClient) -> Account:
    return get_localnet_default_account(algod_client)


@pytest.fixture(scope="session")
def delegated_account(
    delegating_account: Account, lsig_template: str, algod_client: AlgodClient
) -> LogicSig:
    assert is_localnet(algod_client)

    sp = algod_client.suggested_params()
    rendered = algokit_utils.deploy.replace_template_variables(
        lsig_template,
        {
            "LAST_ROUND": sp.first + 1,
            "TARGET_NETWORK_GENESIS": base64.b64decode(sp.gh),
        },
    )
    lsig_delegated = LogicSig(
        base64.b64decode(algod_client.compile(rendered)["result"])
    )
    lsig_delegated.sign(delegating_account.signer.private_key)

    return lsig_delegated


def test_self_payment(
    delegating_account: Account, delegated_account: LogicSig, algod_client: AlgodClient
) -> None:
    sp = algod_client.suggested_params()
    sp.last = sp.first + 1
    delegated_transaction = LogicSigTransaction(
        transaction=PaymentTxn(
            sender=delegating_account.address,
            sp=sp,
            receiver=delegating_account.address,
            amt=0,
            lease=sha256(b"self-payment").digest(),
        ),
        lsig=delegated_account,
    )

    wait_handle = algod_client.send_transaction(delegated_transaction)
    wait_for_confirmation(algod_client, wait_handle)
