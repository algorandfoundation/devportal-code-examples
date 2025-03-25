from typing import NamedTuple

from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    AssetCreateParams,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SigningAccount,
)

from smart_contracts.artifacts.reference_account.reference_account_client import (
    ReferenceAccountClient,
    ReferenceAccountFactory,
)
from smart_contracts.artifacts.reference_account_app.my_counter_client import (
    MyCounterFactory,
)
from smart_contracts.artifacts.reference_account_app.reference_account_app_client import (
    ReferenceAccountAppClient,
    ReferenceAccountAppFactory,
)
from smart_contracts.artifacts.reference_account_asset.reference_account_asset_client import (
    ReferenceAccountAssetClient,
    ReferenceAccountAssetFactory,
)
from smart_contracts.artifacts.reference_app.reference_app_client import (
    ReferenceAppClient,
    ReferenceAppFactory,
)
from smart_contracts.artifacts.reference_app_box.reference_app_box_client import (
    ReferenceAppBoxClient,
    ReferenceAppBoxFactory,
)
from smart_contracts.artifacts.reference_asset.reference_asset_client import (
    ReferenceAssetClient,
    ReferenceAssetFactory,
)


# Define the named tuple type with proper type hints
class LocalnetEnvironment(NamedTuple):
    algorand_client: AlgorandClient
    dispenser: SigningAccount
    account_a: SigningAccount
    account_b: SigningAccount
    account_c: SigningAccount
    account_d: SigningAccount
    reference_account: SigningAccount
    reference_account_app_client: ReferenceAccountClient
    reference_asset_app_client: ReferenceAssetClient
    reference_asset_id: int
    reference_app_app_client: ReferenceAppClient
    account_asset_reference_app_client: ReferenceAccountAssetClient
    reference_account_app_app_client: ReferenceAccountAppClient
    reference_app_box_app_client: ReferenceAppBoxClient


def bootstrap_reference_account_example(
    algorand: AlgorandClient, account: SigningAccount
) -> tuple[SigningAccount, ReferenceAccountClient]:
    # Create an account from mnemonic for reference examples
    reference_account = algorand.account.from_mnemonic(
        mnemonic="rice broken rail solve mobile pill glue maximum speak mean stumble orbit mixed empower rent congress nest input peanut crush comfort spell swear abandon actual"
    )

    factory = algorand.client.get_typed_app_factory(
        ReferenceAccountFactory,
        default_sender=account.address,
    )
    client, deploy_result = factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    return reference_account, client


def bootstrap_reference_asset_example(
    algorand: AlgorandClient, account: SigningAccount
) -> tuple[ReferenceAssetClient, int]:
    result = algorand.send.asset_create(
        AssetCreateParams(
            sender=account.address,
            total=1_000_000,
            decimals=6,
            asset_name="Reference Asset",
            unit_name="REF",
        )
    )

    factory = algorand.client.get_typed_app_factory(
        ReferenceAssetFactory,
        default_sender=account.address,
    )
    client, deploy_result = factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    return client, result.asset_id


def bootstrap_reference_app_example(
    algorand: AlgorandClient, account: SigningAccount
) -> ReferenceAppClient:
    factory = algorand.client.get_typed_app_factory(
        ReferenceAppFactory,
        default_sender=account.address,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    return client


def bootstrap_account_asset_reference_example(
    algorand: AlgorandClient, account: SigningAccount
) -> ReferenceAccountAssetClient:
    factory = algorand.client.get_typed_app_factory(
        ReferenceAccountAssetFactory,
        default_sender=account.address,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    return client


def bootstrap_reference_account_app_example(
    algorand: AlgorandClient, account: SigningAccount
) -> ReferenceAccountAppClient:

    counter_factory = algorand.client.get_typed_app_factory(
        MyCounterFactory,
        default_sender=account.address,
    )

    counter_client, deploy_result = counter_factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    factory = algorand.client.get_typed_app_factory(
        ReferenceAccountAppFactory,
        default_sender=account.address,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    return client


def bootstrap_app_box_example(
    algorand: AlgorandClient, account: SigningAccount
) -> ReferenceAppBoxClient:
    factory = algorand.client.get_typed_app_factory(
        ReferenceAppBoxFactory,
        default_sender=account.address,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.AppendApp, on_schema_break=OnSchemaBreak.AppendApp
    )

    return client


def setup_localnet_environment() -> LocalnetEnvironment:
    """
    Sets up an Algorand client configured for LocalNet,
    creates a dispenser account and several random test accounts,
    and sends a small payment to each test account.

    Returns:
        LocalnetEnvironment: A named tuple containing:
            - algorand_client: The client instance for LocalNet.
            - dispenser: The localnet dispenser account.
            - account_a: The first test account.
            - account_b: The second test account.
            - account_c: The third test account.
            - and more helper clients and resources
    """
    # Initialize an Algorand client instance configured for LocalNet.
    algorand_client = AlgorandClient.default_localnet()
    algorand_client.set_suggested_params_cache_timeout(0)

    # Retrieve the localnet dispenser account.
    dispenser = algorand_client.account.localnet_dispenser()

    # Create random accounts for testing or development.
    account_a = algorand_client.account.random()
    account_b = algorand_client.account.random()
    account_c = algorand_client.account.random()
    account_d = algorand_client.account.random()
    accounts = [account_a, account_b, account_c, account_d]

    # Fund each test account with a small payment.
    for account in accounts:
        algorand_client.send.payment(
            PaymentParams(
                sender=dispenser.address,
                receiver=account.address,
                amount=AlgoAmount(algo=10),
            )
        )

    # Create other apps, accounts and assets related to examples
    reference_account, reference_account_app_client = (
        bootstrap_reference_account_example(algorand_client, dispenser)
    )
    reference_asset_app_client, reference_asset_id = bootstrap_reference_asset_example(
        algorand_client, dispenser
    )
    reference_app_app_client = bootstrap_reference_app_example(
        algorand_client, dispenser
    )
    account_asset_reference_app_client = bootstrap_account_asset_reference_example(
        algorand_client, dispenser
    )
    reference_account_app_app_client = bootstrap_reference_account_app_example(
        algorand_client, dispenser
    )
    reference_app_box_app_client = bootstrap_app_box_example(algorand_client, dispenser)

    # Return a properly typed named tuple
    return LocalnetEnvironment(
        algorand_client=algorand_client,
        dispenser=dispenser,
        account_a=account_a,
        account_b=account_b,
        account_c=account_c,
        account_d=account_d,
        reference_account=reference_account,
        reference_account_app_client=reference_account_app_client,
        reference_asset_app_client=reference_asset_app_client,
        reference_asset_id=reference_asset_id,
        reference_app_app_client=reference_app_app_client,
        account_asset_reference_app_client=account_asset_reference_app_client,
        reference_account_app_app_client=reference_account_app_app_client,
        reference_app_box_app_client=reference_app_box_app_client,
    )
