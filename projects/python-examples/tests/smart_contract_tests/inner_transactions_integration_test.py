import pytest
from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    CommonAppCallParams,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SigningAccount,
)
from algokit_utils.config import config

from smart_contracts.artifacts.hello_world.hello_world_client import (
    HelloWorldFactory,
)
from smart_contracts.artifacts.inner_transactions.inner_transactions_client import (
    AssetConfigArgs,
    AssetDeleteArgs,
    AssetFreezeArgs,
    AssetOptInArgs,
    AssetRevokeArgs,
    AssetTransferArgs,
    InnerTransactionsClient,
    InnerTransactionsFactory,
    MultiInnerTxnsArgs,
    NoopAppCallArgs,
)


@pytest.fixture(scope="session")
def creator_inner_txn_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> InnerTransactionsClient:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        InnerTransactionsFactory,
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
def hello_world_app_id(creator: SigningAccount, algorand: AlgorandClient) -> int:
    """Deploy the inner txn App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        HelloWorldFactory,
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

    return client.app_id


@pytest.fixture(scope="session")
def optin_example_asset_id(creator: SigningAccount, algorand: AlgorandClient) -> int:
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
    return sent_txn.asset_id


@pytest.fixture(scope="session")
def test_asset_create(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> int:

    txn_result = creator_inner_txn_app_client.send.non_fungible_asset_create(
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000))
    )

    app_acct_info = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    )
    asset_info = app_acct_info.assets
    assert asset_info is not None, "Expected asset list from account information"
    assert len(asset_info) > 0
    for asset in asset_info:
        if asset["asset-id"] == txn_result.abi_return:
            assert asset["asset-id"] == txn_result.abi_return
    assert txn_result.abi_return is not None

    return txn_result.abi_return


def test_fungible_asset_create(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> None:

    txn_result = creator_inner_txn_app_client.send.fungible_asset_create(
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000))
    )

    app_acct_info = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    )
    asset_info = app_acct_info.assets
    assert asset_info is not None, "Expected asset list from account information"
    assert len(asset_info) > 0
    assert any(asset["asset-id"] == txn_result.abi_return for asset in asset_info)


def test_payment(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> None:

    txn_result = creator_inner_txn_app_client.send.payment(
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000))
    )

    assert txn_result.abi_return == 5000


def test_asset_opt_in(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    optin_example_asset_id: int,
) -> None:

    creator_inner_txn_app_client.send.asset_opt_in(
        AssetOptInArgs(asset=optin_example_asset_id),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )
    assets = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    ).assets
    assert assets is not None, "Expected assets list"
    assert assets[1]["amount"] == 0


def test_asset_transfer(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    alice: SigningAccount,
) -> None:

    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=alice.address,
            asset_id=test_asset_create,
        )
    )

    txn_result = creator_inner_txn_app_client.send.asset_transfer(
        AssetTransferArgs(asset=test_asset_create, receiver=alice.address, amount=1),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )

    alice_asset_info = algorand.account.get_information(alice.address).assets
    assert alice_asset_info is not None, "Expected alice asset info"
    assert alice_asset_info[0]["asset-id"] == test_asset_create
    assert alice_asset_info[0]["amount"] == 1


def test_asset_freeze(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    alice: SigningAccount,
) -> None:

    creator_inner_txn_app_client.send.asset_freeze(
        AssetFreezeArgs(acct_to_be_frozen=alice.address, asset=test_asset_create),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )

    alice_asset_info = algorand.account.get_information(alice.address).assets
    assert alice_asset_info is not None, "Expected alice asset info"
    assert alice_asset_info[0]["is-frozen"]


def test_asset_revoke(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    alice: SigningAccount,
) -> None:

    creator_inner_txn_app_client.send.asset_revoke(
        AssetRevokeArgs(
            asset=test_asset_create, account_to_be_revoked=alice.address, amount=1
        ),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )

    alice_asset_info = algorand.account.get_information(alice.address).assets
    assert alice_asset_info is not None, "Expected alice asset info"
    assert alice_asset_info[0]["amount"] == 0


def test_asset_config(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
    creator: SigningAccount,
) -> None:

    creator_inner_txn_app_client.send.asset_config(
        AssetConfigArgs(asset=test_asset_create),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )

    app_asset_info = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    ).created_assets
    assert app_asset_info is not None, "Expected created assets list"
    assert app_asset_info[1]["params"]["freeze"] == creator.address
    assert app_asset_info[1]["params"]["clawback"] == creator.address


def test_asset_delete(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    test_asset_create: int,
) -> None:

    creator_inner_txn_app_client.send.asset_delete(
        AssetDeleteArgs(asset=test_asset_create),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )

    app_acct_info = algorand.account.get_information(
        creator_inner_txn_app_client.app_address
    )
    asset_info = app_acct_info.assets
    assert asset_info is not None, "Expected assets list from account information"
    assert not any(asset["asset-id"] == test_asset_create for asset in asset_info)


def test_multi_inner_txns(
    creator_inner_txn_app_client: InnerTransactionsClient,
    hello_world_app_id: int,
) -> None:

    txn_result = creator_inner_txn_app_client.send.multi_inner_txns(
        MultiInnerTxnsArgs(app_id=hello_world_app_id),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=2000)),
    )

    assert txn_result.abi_return is not None, "Expected abi_return tuple"
    assert txn_result.abi_return[0] == 5000
    assert txn_result.abi_return[1] == "Hello, World"


def test_deploy_app(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
) -> None:

    txn_result = creator_inner_txn_app_client.send.deploy_app(
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000)),
    )


def test_no_op_app_calls(
    algorand: AlgorandClient,
    creator_inner_txn_app_client: InnerTransactionsClient,
    hello_world_app_id: int,
) -> None:

    txn_result = creator_inner_txn_app_client.send.noop_app_call(
        NoopAppCallArgs(app_id=hello_world_app_id),
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=2000)),
    )

    assert txn_result.abi_return is not None, "Expected abi_return tuple"
    assert txn_result.abi_return[0] == "Hello, World"
    assert txn_result.abi_return[1] == "Hello, again"
