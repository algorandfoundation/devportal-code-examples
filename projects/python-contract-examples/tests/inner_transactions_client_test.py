import pytest
from algokit_utils import TransactionParameters
from algokit_utils.beta.account_manager import AddressAndSigner
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    PayParams,
)
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient

from smart_contracts.artifacts.hello_world.hello_world_client import HelloWorldClient
from smart_contracts.artifacts.inner_transactions.inner_transactions_client import (
    InnerTransactionsClient,
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
def alice(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    """Get an account to use as Alice who will participate in the auction"""
    acct = algorand.account.random()

    # Make sure the account has some ALGO
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )

    return acct


@pytest.fixture(scope="session")
def creator_inner_txn_app_client(
    algod_client: AlgodClient, creator: AddressAndSigner, algorand: AlgorandClient
) -> InnerTransactionsClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = InnerTransactionsClient(
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
def hello_world_app_id(
    algod_client: AlgodClient, creator: AddressAndSigner
) -> HelloWorldClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = HelloWorldClient(
        algod_client,
        sender=creator.address,
        signer=creator.signer,
    )

    client.create_bare()

    print(f"Hello World App Id: {client.app_id}")
    return client.app_id


@pytest.fixture(scope="session")
def optin_example_asset_id(creator: AddressAndSigner, algorand: AlgorandClient) -> int:
    """Create an asset to be auctioned"""
    # Create an asset
    sent_txn = algorand.send.asset_create(
        AssetCreateParams(
            sender=creator.address,
            total=1,
            decimals=0,
            asset_name="MyAsset",
            unit_name="MA",
            url="https://path/to/my/asset/details",
        )
    )

    # Make sure the network tells us the ID of the asset we just created
    return sent_txn["confirmation"]["asset-index"]


@pytest.fixture(scope="session")
def test_asset_create(
    algorand: AlgorandClient,
    algod_client: AlgodClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> None:
    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    txn_result = creator_inner_txn_app_client.asset_create(
        transaction_parameters=TransactionParameters(suggested_params=sp)
    )
    print(f"Created Asset ID: {txn_result.return_value}")

    app_acct_info = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    )
    asset_info: list = app_acct_info["assets"]
    assert len(asset_info) > 0
    assert asset_info[1]["asset-id"] == txn_result.return_value

    return txn_result.return_value


def test_payment(
    algod_client: AlgodClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    txn_result = creator_inner_txn_app_client.payment(
        transaction_parameters=TransactionParameters(suggested_params=sp)
    )
    print(f"Payment amount: {txn_result.return_value}")

    assert txn_result.return_value == 5000


def test_asset_opt_in(
    algod_client: AlgodClient,
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    optin_example_asset_id: int,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    creator_inner_txn_app_client.asset_opt_in(
        asset=optin_example_asset_id,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )
    app_acct_info = algorand.account.get_asset_information(
        creator_inner_txn_app_client.app_address, optin_example_asset_id
    )

    assert app_acct_info["asset-holding"]["amount"] == 0


def test_asset_transfer(
    algod_client: AlgodClient,
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    alice: AddressAndSigner,
) -> None:

    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=alice.address,
            asset_id=test_asset_create,
        )
    )

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    creator_inner_txn_app_client.asset_transfer(
        asset=test_asset_create,
        receiver=alice.address,
        amount=1,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )

    alice_asset_info = algorand.account.get_asset_information(
        alice.address, test_asset_create
    )

    assert alice_asset_info["asset-holding"]["asset-id"] == test_asset_create
    assert alice_asset_info["asset-holding"]["amount"] == 1


def test_asset_freeze(
    algod_client: AlgodClient,
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    alice: AddressAndSigner,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    creator_inner_txn_app_client.asset_freeze(
        acct_to_be_frozen=alice.address,
        asset=test_asset_create,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )

    alice_asset_info = algorand.account.get_asset_information(
        alice.address, test_asset_create
    )

    assert alice_asset_info["asset-holding"]["is-frozen"]


def test_asset_revoke(
    algod_client: AlgodClient,
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    alice: AddressAndSigner,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    creator_inner_txn_app_client.asset_revoke(
        asset=test_asset_create,
        account_to_be_revoked=alice.address,
        amount=1,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )

    alice_asset_info = algorand.account.get_asset_information(
        alice.address, test_asset_create
    )

    assert alice_asset_info["asset-holding"]["amount"] == 0


def test_asset_config(
    algod_client: AlgodClient,
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    creator: AddressAndSigner,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    creator_inner_txn_app_client.asset_config(
        asset=test_asset_create,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )

    app_asset_info = algorand.account.get_asset_information(
        creator_inner_txn_app_client.app_address, test_asset_create
    )

    assert app_asset_info["created-asset"]["freeze"] == creator.address
    assert app_asset_info["created-asset"]["clawback"] == creator.address


def test_asset_delete(
    algod_client: AlgodClient,
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    creator_inner_txn_app_client.asset_delete(
        asset=test_asset_create,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )

    app_acct_info = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    )
    asset_info: list = app_acct_info["assets"]

    assert len(asset_info) == 1


def test_multi_inner_txns(
    algod_client: AlgodClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    hello_world_app_id: int,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 3000  # cover two inner transactions

    txn_result = creator_inner_txn_app_client.multi_inner_txns(
        app_id=hello_world_app_id,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )
    print(f"multi_inner_txns result: {txn_result.return_value}")

    assert txn_result.return_value[0] == 5000
    assert txn_result.return_value[1] == "Hello, World"


def test_deploy_app(
    algod_client: AlgodClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000

    txn_result = creator_inner_txn_app_client.deploy_app(
        transaction_parameters=TransactionParameters(suggested_params=sp)
    )
    print(f"Deployed App ID: {txn_result.return_value}")


def test_no_op_app_calls(
    algod_client: AlgodClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    hello_world_app_id: int,
) -> None:

    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 3000  # cover two inner transactions

    txn_result = creator_inner_txn_app_client.noop_app_call(
        app_id=hello_world_app_id,
        transaction_parameters=TransactionParameters(suggested_params=sp),
    )
    print(f"multi_inner_txns result: {txn_result.return_value}")

    assert txn_result.return_value[0] == "Hello, World"
    assert txn_result.return_value[1] == "Hello, again"
