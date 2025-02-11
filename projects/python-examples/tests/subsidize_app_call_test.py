import base64

import algokit_utils.applications
import algokit_utils.applications.app_manager
import algokit_utils
from algokit_utils.models.account import LogicSigAccount

import algosdk

import pytest

from smart_contracts.artifacts.hello_world.hello_world_client import (
    HelloArgs,
    HelloWorldClient,
    HelloWorldFactory,
)


# TODO: update to utils v3
@pytest.fixture(scope="session")
def lsig_template() -> str:
    with open(
        "./smart_contracts/artifacts/subsidize_app_call/subsidize_app_call.teal"
    ) as f:
        return f.read()


@pytest.fixture(scope="session")
def hello_world_client(
    algorand: algokit_utils.AlgorandClient, creator: algokit_utils.SigningAccount
) -> HelloWorldClient:

    factory = algorand.client.get_typed_app_factory(
        HelloWorldFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=algokit_utils.OnUpdate.ReplaceApp,
        on_schema_break=algokit_utils.OnSchemaBreak.Fail,
    )

    return client


@pytest.fixture(scope="session")
def contract_account(
    lsig_template: str,
    algorand: algokit_utils.AlgorandClient,
    hello_world_client: HelloWorldClient,
    dispenser: algokit_utils.SigningAccount,
) -> LogicSigAccount:

    sp = algorand.get_suggested_params()
    rendered = algokit_utils.applications.AppManager.replace_template_variables(
        lsig_template,
        {
            "EXPIRATION_ROUND": sp.last + 10,
            "TARGET_NETWORK_GENESIS": base64.b64decode(sp.gh),
            "KNOWN_APP": hello_world_client.app_id,
        },
    )
    lsig_account = LogicSigAccount(
        algosdk.transaction.LogicSigAccount(
            base64.b64decode(algorand.client.algod.compile(rendered)["result"])
        )
    )
    algorand.account.ensure_funded(
        account_to_fund=lsig_account,
        dispenser_account=dispenser,
        min_spending_balance=algokit_utils.AlgoAmount(algo=2),
    )
    return lsig_account


def test_subsidize_fee(
    contract_account: LogicSigAccount,
    hello_world_client: HelloWorldClient,
    algorand: algokit_utils.AlgorandClient,
) -> None:

    # The LSIG provides fees for both transactions in the group. This does not need a digital signature.
    # It is the code associated with the Contract Account that validates the second transaction and
    #  allows it to be executed with the Contract Account as the sender.
    subsidize_pay_txn = algorand.create_transaction.payment(
        algokit_utils.PaymentParams(
            sender=contract_account.address,
            signer=contract_account.signer,
            receiver=contract_account.address,
            amount=algokit_utils.AlgoAmount(algo=0),
            extra_fee=algokit_utils.ALGORAND_MIN_TX_FEE,
        ),
    )

    # The app caller provides 0 fees.
    hello_world_client.new_group().hello(
        HelloArgs(name="Juan"),
        params=algokit_utils.CommonAppCallParams(
            static_fee=algokit_utils.AlgoAmount(algo=0)
        ),
    ).add_transaction(subsidize_pay_txn, signer=contract_account.signer).send()
