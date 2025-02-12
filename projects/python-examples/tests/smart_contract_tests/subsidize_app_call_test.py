import base64

import pytest
from algokit_utils import (
    ALGORAND_MIN_TX_FEE,
    AlgoAmount,
    AlgorandClient,
    CommonAppCallParams,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SigningAccount,
)
from algokit_utils.applications import AppManager
from algokit_utils.models.account import LogicSigAccount

from smart_contracts.artifacts.hello_world.hello_world_client import (
    HelloArgs,
    HelloWorldClient,
    HelloWorldFactory,
)


# TODO: wait for rekey operation updates to utils py
@pytest.fixture(scope="session")
def lsig_template() -> str:
    with open(
        "./smart_contracts/artifacts/subsidize_app_call/subsidize_app_call.teal"
    ) as f:
        return f.read()


@pytest.fixture(scope="session")
def hello_world_client(
    algorand: AlgorandClient, creator: SigningAccount
) -> HelloWorldClient:

    factory = algorand.client.get_typed_app_factory(
        HelloWorldFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    return client


@pytest.fixture(scope="session")
def contract_account(
    lsig_template: str,
    algorand: AlgorandClient,
    hello_world_client: HelloWorldClient,
    dispenser: SigningAccount,
) -> LogicSigAccount:

    sp = algorand.get_suggested_params()
    rendered = AppManager.replace_template_variables(
        lsig_template,
        {
            "EXPIRATION_ROUND": sp.last + 10,
            "TARGET_NETWORK_GENESIS": base64.b64decode(sp.gh),
            "KNOWN_APP": hello_world_client.app_id,
        },
    )
    compiled_lsig_program = algorand.app.compile_teal(rendered).compiled_base64_to_bytes
    lsig_account = algorand.account.logicsig(compiled_lsig_program)

    algorand.account.ensure_funded(
        account_to_fund=lsig_account,
        dispenser_account=dispenser,
        min_spending_balance=AlgoAmount(algo=2),
    )
    return lsig_account


def test_subsidize_fee(
    contract_account: LogicSigAccount,
    hello_world_client: HelloWorldClient,
    algorand: AlgorandClient,
) -> None:

    # The LSIG provides fees for both transactions in the group. This does not need a digital signature.
    # It is the code associated with the Contract Account that validates the second transaction and
    #  allows it to be executed with the Contract Account as the sender.
    subsidize_pay_txn = algorand.create_transaction.payment(
        PaymentParams(
            sender=contract_account.address,
            signer=contract_account.signer,
            receiver=contract_account.address,
            amount=AlgoAmount(algo=0),
            extra_fee=ALGORAND_MIN_TX_FEE,
        ),
    )

    # The app caller provides 0 fees.
    hello_world_client.new_group().hello(
        HelloArgs(name="Juan"),
        params=CommonAppCallParams(static_fee=AlgoAmount(algo=0)),
    ).add_transaction(subsidize_pay_txn, signer=contract_account.signer).send()
