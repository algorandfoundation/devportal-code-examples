import base64
from copy import deepcopy

import algokit_utils
import pytest
from algokit_utils import (
    EnsureBalanceParameters,
    TransactionParameters,
    ensure_funded,
    get_localnet_default_account,
    is_localnet,
)
from algosdk.atomic_transaction_composer import (
    LogicSigTransactionSigner,
    TransactionWithSigner,
)
from algosdk.constants import MIN_TXN_FEE
from algosdk.transaction import LogicSigAccount, PaymentTxn
from algosdk.util import algos_to_microalgos
from algosdk.v2client.algod import AlgodClient

from smart_contracts.artifacts.hello_world.hello_world_client import HelloWorldClient


@pytest.fixture(scope="session")
def lsig_template() -> str:
    with open(
        "./smart_contracts/artifacts/subsidize_app_call/subsidize_app_call.teal"
    ) as f:
        return f.read()


@pytest.fixture(scope="session")
def hello_world_client(algod_client: AlgodClient) -> HelloWorldClient:
    client = HelloWorldClient(
        algod_client, signer=get_localnet_default_account(algod_client)
    )

    client.create_bare()

    return client


@pytest.fixture(scope="session")
def contract_account(
    lsig_template: str, algod_client: AlgodClient, hello_world_client: HelloWorldClient
) -> LogicSigAccount:
    assert is_localnet(algod_client)

    sp = algod_client.suggested_params()
    rendered = algokit_utils.deploy.replace_template_variables(
        lsig_template,
        {
            "EXPIRATION_ROUND": sp.last + 10,
            "TARGET_NETWORK_GENESIS": base64.b64decode(sp.gh),
            "KNOWN_APP": hello_world_client.app_id,
        },
    )
    lsig_account = LogicSigAccount(
        base64.b64decode(algod_client.compile(rendered)["result"])
    )
    ensure_funded(
        algod_client,
        EnsureBalanceParameters(
            account_to_fund=lsig_account.address(),
            min_spending_balance_micro_algos=algos_to_microalgos(2),
        ),
    )

    return lsig_account


@pytest.fixture(scope="session")
def contract_account_signer(
    contract_account: LogicSigAccount,
) -> LogicSigTransactionSigner:
    return LogicSigTransactionSigner(contract_account)


def test_subsidize_fee(
    contract_account_signer: LogicSigTransactionSigner,
    hello_world_client: HelloWorldClient,
) -> None:
    # The app caller provides 0 fees.
    sp_call = hello_world_client.algod_client.suggested_params()
    sp_call.flat_fee = True
    sp_call.fee = 0
    atc = (
        hello_world_client.compose()
        .hello(
            name="Juan",
            transaction_parameters=TransactionParameters(suggested_params=sp_call),
        )
        .atc
    )

    # The LSIG provides fees for both transactions in the group. This does not need a digital signature.
    # It is the code associated with the Contract Account that validates the second transaction and
    #  allows it to be executed with the Contract Account as the sender.
    sp_lsig = deepcopy(sp_call)
    sp_lsig.flat_fee = True
    sp_lsig.fee = 2 * MIN_TXN_FEE
    atc.add_transaction(
        TransactionWithSigner(
            txn=PaymentTxn(
                sender=contract_account_signer.lsig.address(),
                sp=sp_lsig,
                receiver=contract_account_signer.lsig.address(),
                amt=0,
            ),
            signer=contract_account_signer,
        )
    )
    atc.execute(hello_world_client.algod_client, wait_rounds=1)
