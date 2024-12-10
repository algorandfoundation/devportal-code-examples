import pytest
from algokit_utils.beta.account_manager import AddressAndSigner
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    PayParams,
)
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient

from smart_contracts.artifacts.control_flow import (
    for_loops_example_client,
    if_else_example_client,
    match_statements_client,
    while_loop_example_client,
)


@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Get an AlgorandClient to use throughout the tests"""
    algorand = AlgorandClient.default_local_net()
    algorand.set_default_validity_window(1000)

    return algorand


@pytest.fixture(scope="session")
def dispenser(algorand: AlgorandClient) -> AddressAndSigner:
    """Get the dispenser to fund test addresses"""
    return algorand.account.dispenser()


@pytest.fixture(scope="session")
def creator(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    """Get an account to use as the creator of the inner transaction contract"""
    acct = algorand.account.random()

    # Make sure the account has some ALGO
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )

    return acct


@pytest.fixture(scope="session")
def if_else_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> if_else_example_client.IfElseExampleClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = if_else_example_client.IfElseExampleClient(
        algod_client,
        sender=creator.address,
        signer=creator.signer,
    )

    client.create_bare()

    algorand.send.payment(
        PayParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=1000000,  # 1 Algo
        )
    )

    print(f"Inner Txn app ID: {client.app_id}")
    return client


@pytest.fixture(scope="session")
def for_loop_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> for_loops_example_client.ForLoopsExampleClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = for_loops_example_client.ForLoopsExampleClient(
        algod_client,
        sender=creator.address,
        signer=creator.signer,
    )

    client.create_bare()

    algorand.send.payment(
        PayParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=1000000,  # 1 Algo
        )
    )

    print(f"Inner Txn app ID: {client.app_id}")
    return client


@pytest.fixture(scope="session")
def match_statements_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> match_statements_client.MatchStatementsClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = match_statements_client.MatchStatementsClient(
        algod_client,
        sender=creator.address,
        signer=creator.signer,
    )

    client.create_bare()

    algorand.send.payment(
        PayParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=1000000,  # 1 Algo
        )
    )

    print(f"Inner Txn app ID: {client.app_id}")
    return client


@pytest.fixture(scope="session")
def while_loop_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> while_loop_example_client.WhileLoopExampleClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = while_loop_example_client.WhileLoopExampleClient(
        algod_client,
        sender=creator.address,
        signer=creator.signer,
    )

    client.create_bare()

    algorand.send.payment(
        PayParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=1000000,  # 1 Algo
        )
    )

    print(f"Inner Txn app ID: {client.app_id}")
    return client


def test_if_else(
    if_else_app_client: if_else_example_client.IfElseExampleClient,
) -> None:

    inputs = [
        (1001, "This account is rich!"),
        (101, "This account is doing well."),
        (50, "This account is poor :("),
    ]

    for input_value in inputs:
        txn_result = if_else_app_client.is_rich(account_balance=input_value[0])
        print(f"is_rich result: {txn_result.return_value}")

        assert txn_result.return_value == input_value[1]
    print(f"if_else result: {txn_result.return_value}")

    inputs = [(1, "Odd"), (2, "Even")]
    for i in inputs:
        txn_result = if_else_app_client.is_even(number=i[0])
        print(f"is_even result: {txn_result.return_value}")

        assert txn_result.return_value == i[1]


def test_for_loops(
    for_loop_app_client: for_loops_example_client.ForLoopsExampleClient,
) -> None:

    txn_result = for_loop_app_client.for_loop()
    print(f"for_loop result: {txn_result.return_value}")

    assert txn_result.return_value == [3, 2, 1, 0]


def test_match_statements(
    match_statements_app_client: match_statements_client.MatchStatementsClient,
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
        txn_result = match_statements_app_client.get_day(date=i[0])
        print(f"get_day result: {txn_result.return_value}")

        assert txn_result.return_value == i[1]


def test_while_loop(
    while_loop_app_client: while_loop_example_client.WhileLoopExampleClient,
) -> None:

    txn_result = while_loop_app_client.loop()
    print(f"loop result: {txn_result.return_value}")

    assert txn_result.return_value == 7
