import base64
from hashlib import sha256

from algokit_utils import *
from algokit_utils.models.account import LogicSigAccount
from algokit_utils.applications import AppManager
import pytest

# from algosdk.transaction import (
#     LogicSig,
#     LogicSigTransaction,
#     PaymentTxn,
#     wait_for_confirmation,
# )


@pytest.fixture(scope="session")
def lsig_template() -> str:
    with open("./smart_contracts/artifacts/self_payment/self_payment.teal") as f:
        return f.read()


@pytest.fixture(scope="session")
def delegating_account(creator: SigningAccount) -> SigningAccount:
    return creator


@pytest.fixture(scope="session")
def lsig_delegated_account(
    delegating_account: SigningAccount, lsig_template: str, algorand: AlgorandClient
) -> LogicSigAccount:

    sp = algorand.get_suggested_params()
    rendered = AppManager.replace_template_variables(
        lsig_template,
        {
            "LAST_ROUND": sp.first + 1,
            "TARGET_NETWORK_GENESIS": base64.b64decode(sp.gh),
        },
    )

    lsig_delegated = algorand.account.logicsig(
        base64.b64decode(algorand.client.algod.compile(rendered)["result"])
    )

    # TODO: sign the logic sig

    return lsig_delegated


def test_self_payment(
    delegating_account: SigningAccount,
    lsig_delegated_account: LogicSigAccount,
    algorand: AlgorandClient,
) -> None:

    # TODO: Learn how to construct logic sig transactions
    algorand.create_transaction.payment(
        PaymentParams(
            sender=delegating_account.address,
            signer=lsig_delegated_account,
            receiver=delegating_account.address,
            amount=AlgoAmount(algo=0),
            lease=sha256(b"self-payment").digest(),
        )
    )

    # delegated_transaction = LogicSigTransaction(
    #     transaction=PaymentTxn(
    #         sender=delegating_account.address,
    #         sp=sp,
    #         receiver=delegating_account.address,
    #         amt=0,
    #         lease=sha256(b"self-payment").digest(),
    #     ),
    #     lsig=delegated_account,
    # )

    # wait_handle = algod_client.send_transaction(delegated_transaction)
    # wait_for_confirmation(algod_client, wait_handle)
