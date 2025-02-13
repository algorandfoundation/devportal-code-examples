import pytest
from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SigningAccount,
)
from algokit_utils.config import config

from smart_contracts.artifacts.control_flow.for_loops_example_client import (
    ForLoopsExampleClient,
    ForLoopsExampleFactory,
)
from smart_contracts.artifacts.control_flow.if_else_example_client import (
    IfElseExampleClient,
    IfElseExampleFactory,
    IsEvenArgs,
    IsRichArgs,
)
from smart_contracts.artifacts.control_flow.match_statements_client import (
    GetDayArgs,
    MatchStatementsClient,
    MatchStatementsFactory,
)
from smart_contracts.artifacts.control_flow.while_loop_example_client import (
    WhileLoopExampleClient,
    WhileLoopExampleFactory,
)


@pytest.fixture(scope="session")
def if_else_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> IfElseExampleClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        IfElseExampleFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def for_loop_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> ForLoopsExampleClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        ForLoopsExampleFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def match_statements_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> MatchStatementsClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        MatchStatementsFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def while_loop_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> WhileLoopExampleClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        WhileLoopExampleFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


def test_if_else(
    if_else_app_client: IfElseExampleClient,
) -> None:

    inputs = [
        (1001, "This account is rich!"),
        (101, "This account is doing well."),
        (50, "This account is poor :("),
    ]

    for input_value in inputs:
        txn_result = if_else_app_client.send.is_rich(
            IsRichArgs(account_balance=input_value[0])
        )
        print(f"is_rich result: {txn_result.abi_return}")

        assert txn_result.abi_return == input_value[1]
    print(f"if_else result: {txn_result.abi_return}")

    inputs = [(1, "Odd"), (2, "Even")]
    for i in inputs:
        txn_result = if_else_app_client.send.is_even(IsEvenArgs(number=i[0]))
        print(f"is_even result: {txn_result.abi_return}")

        assert txn_result.abi_return == i[1]


def test_for_loops(
    for_loop_app_client: ForLoopsExampleClient,
) -> None:

    txn_result = for_loop_app_client.send.for_loop()
    print(f"for_loop result: {txn_result.abi_return}")

    assert txn_result.abi_return is not None, "Expected ABI return from for_loop"
    assert txn_result.abi_return == [3, 2, 1, 0]  # type: ignore[comparison-overlap]


def test_match_statements(
    match_statements_app_client: MatchStatementsClient,
) -> None:

    inputs = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
        (7, "Invalid day"),
    ]

    for i in inputs:
        txn_result = match_statements_app_client.send.get_day(GetDayArgs(date=i[0]))
        print(f"get_day result: {txn_result.abi_return}")

        assert txn_result.abi_return == i[1]


def test_while_loop(
    while_loop_app_client: WhileLoopExampleClient,
) -> None:

    txn_result = while_loop_app_client.send.loop()
    print(f"loop result: {txn_result.abi_return}")

    assert txn_result.abi_return == 7
