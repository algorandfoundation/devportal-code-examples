import pytest
from algokit_utils.beta.account_manager import AddressAndSigner
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    PayParams,
)
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient

from smart_contracts.artifacts.arc4_types.arc4_static_array_client import (
    Arc4StaticArrayClient,
)
from smart_contracts.artifacts.arc4_types.arc4_struct_client import Arc4StructClient
from smart_contracts.artifacts.arc4_types.arc4_types_client import Arc4TypesClient


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
    """Get an account to use as the creator of the contract"""
    acct = algorand.account.random()

    # Make sure the account has some ALGO
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )

    return acct


@pytest.fixture(scope="session")
def alice(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    """Get an account to use as Alice who will participate in the auction"""
    acct = algorand.account.random()

    # Make sure the account has some ALGO
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )

    return acct


@pytest.fixture(scope="session")
def arc4_statc_array_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> Arc4StaticArrayClient:
    """Deploy the arc4 static array App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = Arc4StaticArrayClient(
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

    return client


@pytest.fixture(scope="session")
def arc4_struct_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> Arc4StructClient:
    """Deploy the arc4 struct App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = Arc4StructClient(
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

    return client


@pytest.fixture(scope="session")
def arc4_types_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> Arc4TypesClient:
    """Deploy the arc4 types App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = Arc4TypesClient(
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

    return client


def test_arc4_uint64(
    arc4_types_app_client: Arc4TypesClient,
) -> None:
    """Test the arc4_uint64 method"""

    # Call the arc4_uint64 method
    result = arc4_types_app_client.arc4_uint64(a=1, b=2)

    # Check the result
    assert result.return_value == 3


def test_arc4_address_properties(
    arc4_types_app_client: Arc4TypesClient,
    creator: AddressAndSigner,
    algorand: AlgorandClient,
) -> None:
    """Test the arc4_address_properties method"""

    # Call the arc4_address method
    result = arc4_types_app_client.arc4_address_properties(address=creator.address)

    creator_info = algorand.account.get_information(creator.address)

    assert result.return_value == creator_info["amount"]


def test_arc4_address_return(
    arc4_types_app_client: Arc4TypesClient, creator: AddressAndSigner
) -> None:
    """Test the arc4_address_return method"""

    # Call the arc4_address method
    result = arc4_types_app_client.arc4_address_return(address=creator.address)

    # Check the result
    assert result.return_value == creator.address


def test_arc4_static_array(arc4_statc_array_app_client: Arc4StaticArrayClient) -> None:
    """Test the arc4_static_array method"""

    # Call the arc4_static_array method
    arc4_statc_array_app_client.arc4_static_array()


def test_arc4_struct_add_todo(arc4_struct_app_client: Arc4StructClient) -> None:
    """Test the add_todo method"""

    # Call the add_todo method
    result = arc4_struct_app_client.add_todo(task="wash the dishes")

    assert result.return_value[0][0] == "wash the dishes"
    assert result.return_value[0][1] is False
    assert len(result.return_value) == 1


def test_arc4_struct_complete_and_return_todo(
    arc4_struct_app_client: Arc4StructClient,
) -> None:
    """Test the complete_todo method"""

    # Call the add_todo method
    result = arc4_struct_app_client.add_todo(task="walk my dogs")

    result = arc4_struct_app_client.return_todo(task="walk my dogs")

    # Check the result
    assert result.return_value.task == "walk my dogs"
    assert result.return_value.completed is False

    # Call the complete_todo method
    arc4_struct_app_client.complete_todo(task="walk my dogs")

    result = arc4_struct_app_client.return_todo(task="walk my dogs")

    # Check the result
    assert result.return_value.task == "walk my dogs"
    assert result.return_value.completed is True
