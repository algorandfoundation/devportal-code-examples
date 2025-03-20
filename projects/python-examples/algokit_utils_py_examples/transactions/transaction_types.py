import algosdk
from algokit_utils import (
    AlgoAmount,
    AppCallParams,
    AppCreateParams,
    AppDeleteParams,
    AppUpdateParams,
    AssetConfigParams,
    AssetCreateParams,
    AssetDestroyParams,
    AssetFreezeParams,
    AssetOptInParams,
    AssetOptOutParams,
    AssetTransferParams,
    OfflineKeyRegistrationParams,
    OnlineKeyRegistrationParams,
    PaymentParams,
)

from algokit_utils_py_examples.helpers import setup_localnet_environment


def transaction_types() -> None:
    # example: TRANSACTION_TYPES

    algorand_client, _, account_a, account_b, account_c = setup_localnet_environment()

    # example: PAYMENT_TRANSACTION

    """
    Create a unsigned payment transaction sending 1 Algo from account_a to account_b

    Parameters for a payment transaction.
    - sender: The address of the account that will send the Algo
    - receiver: The address of the account that will receive the Algo
    - amount: Amount to send
    """
    payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
        )
    )

    # example: PAYMENT_TRANSACTION

    # example: ASSET_TRANSFER_TRANSACTION

    """
    Create an unsigned asset transfer transaction of 1 asset with asset id 1234 from account_a to account_b

    Parameters for an asset transfer transaction.
    - sender: The address of the account that will send the asset
    - asset_id: The asset id of the asset to transfer
    - amount: Amount of the asset to transfer (smallest divisible unit)
    - receiver: The address of the account to send the asset to
    """
    asset_transfer_txn = algorand_client.create_transaction.asset_transfer(
        AssetTransferParams(
            sender=account_a.address,
            asset_id=1234,
            receiver=account_b.address,
            amount=1,
        )
    )

    # example: ASSET_TRANSFER_TRANSACTION

    # example: ASSET_OPT_IN_TRANSACTION

    """
    Create an unsigned asset opt in transaction for account_a opting in to asset with asset id 1234

    Parameters for an asset opt in transaction.
    - sender: The address of the account that will opt in to the asset
    - asset_id: ID of the asset
    """
    asset_opt_in_txn = algorand_client.create_transaction.asset_opt_in(
        AssetOptInParams(
            sender=account_a.address,
            asset_id=1234,
        )
    )

    # example: ASSET_OPT_IN_TRANSACTION

    # example: ASSET_OPT_OUT_TRANSACTION

    """
    Create an unsigned asset opt out transaction for account_a opting out of asset with asset id 1234

    Parameters for an asset opt out transaction.
    - sender: The address of the account that will opt out of the asset
    - asset_id: ID of the asset
    - creator: The creator address of the asset
    """
    asset_opt_out_txn = algorand_client.create_transaction.asset_opt_out(
        AssetOptOutParams(
            sender=account_a.address,
            asset_id=1234,
            creator=account_b.address,
        )
    )

    # example: ASSET_OPT_OUT_TRANSACTION

    # example: ASSET_CREATE_TRANSACTION

    """
    Create an unsigned asset create transaction creating a fungible ASA with 10 million units

    Parameters for creating a new asset.
    - sender: The address of the account that will send the transaction
    - total: The total amount of the smallest divisible unit to create
    - decimals: The amount of decimal places the asset should have, defaults to None
    - default_frozen: Whether the asset is frozen by default in the creator address, defaults to None
    - manager: The address that can change the manager, reserve, clawback, and freeze addresses, defaults to None
    - reserve: The address that holds the uncirculated supply, defaults to None
    - freeze: The address that can freeze the asset in any account, defaults to None
    - clawback: The address that can clawback the asset from any account, defaults to None
    - unit_name: The short ticker name for the asset, defaults to None
    - asset_name: The full name of the asset, defaults to None
    """
    asset_create_txn = algorand_client.create_transaction.asset_create(
        AssetCreateParams(
            sender=account_a.address,
            total=10_000_000,
            decimals=6,
            default_frozen=False,  # optional
            manager=account_a.address,  # optional. Can be permanently disabled by setting to None
            reserve=account_a.address,  # optional. Can be permanently disabled by setting to None
            freeze=account_a.address,  # optional. Can be permanently disabled by setting to None
            clawback=account_a.address,  # optional. Can be permanently disabled by setting to None
            unit_name="MYA",
            asset_name="My Asset",
        )
    )

    """
    Create an unsigned asset create transaction creating a 1 to 1 unique NFT
    """
    algorand_client.create_transaction.asset_create(
        AssetCreateParams(
            sender=account_a.address,
            total=1,
            asset_name="My NFT",
            unit_name="MNFT",
            decimals=0,
            url="metadata URL",
            metadata_hash=b"Hash of the metadata URL",
        )
    )
    # example: ASSET_CREATE_TRANSACTION

    # example: ASSET_CONFIG_TRANSACTION

    """
    Create an unsigned asset config transaction updating four mutable fields of an asset:
    manager, reserve, freeze, clawback. This operation is only possible if the sender is
    the asset manager and the asset has all four mutable fields set.

    Parameters for configuring an existing asset.
    - sender: The address of the account that will send the transaction
    - asset_id: ID of the asset
    - manager: The address that can change the manager, reserve, clawback, and freeze addresses, defaults to None
    - reserve: The address that holds the uncirculated supply, defaults to None
    - freeze: The address that can freeze the asset in any account, defaults to None
    - clawback: The address that can clawback the asset from any account, defaults to None
    """
    asset_config_txn = algorand_client.create_transaction.asset_config(
        AssetConfigParams(
            sender=account_a.address,
            asset_id=1234,
            manager=account_c.address,
            reserve=account_c.address,
            freeze=account_c.address,
            clawback=account_c.address,
        )
    )

    # example: ASSET_CONFIG_TRANSACTION

    # example: ASSET_FREEZE_TRANSACTION

    """
    Create a unsigned asset freeze transaction freezing an asset with asset id 1234

    Parameters for freezing an asset.
    - sender: The address of the account that will send the transaction
    - asset_id: The ID of the asset
    - account: The account to freeze or unfreeze
    - frozen: Whether the assets in the account should be frozen
    """
    asset_freeze_txn = algorand_client.create_transaction.asset_freeze(
        AssetFreezeParams(
            sender=account_a.address,
            asset_id=1234,
            account=account_b.address,  # The account to freeze or unfreeze
            frozen=True,
        )
    )

    # example: ASSET_FREEZE_TRANSACTION

    # example: ASSET_DESTROY_TRANSACTION

    """
    Create an unsigned asset destroy transaction destroying an asset with asset id 1234
    All of the assets must be owned by the creator of the asset before the asset can be deleted.

    Parameters for destroying an asset.
    - sender: The address of the account that will send the transaction
    - asset_id: ID of the asset
    """
    asset_destroy_txn = algorand_client.create_transaction.asset_destroy(
        AssetDestroyParams(
            sender=account_a.address,
            asset_id=1234,
        )
    )

    # example: ASSET_DESTROY_TRANSACTION

    # example: APPLICATION_CREATE_TRANSACTION

    # Minimal TEAL program that just returns 1 (success)
    minimal_teal = """
    #pragma version 10
    int 1
    return
    """

    """
    Create a unsigned application call transaction calling the hello method on the hello world contract

    Parameters for creating an application.
    - sender: The address of the account that will send the transaction
    - approval_program: The program to execute for all OnCompletes other than ClearState as raw teal (string)
        or compiled teal (bytes)
    - clear_state_program: The program to execute for ClearState OnComplete as raw teal (string)
        or compiled teal (bytes)
    """
    result1 = algorand_client.create_transaction.app_create(
        AppCreateParams(
            sender=account_a.address,
            approval_program=minimal_teal,
            clear_state_program=minimal_teal,
        )
    )

    # example: APPLICATION_CREATE_TRANSACTION

    # example: APPLICATION_NO_OP_TRANSACTION

    """
    Create a unsigned application call transaction with the NoOp OnComplete actions

    Parameters for calling an application.
    - sender: The address of the account that will send the transaction
    - on_complete: The OnComplete action
    - app_id: ID of the application, defaults to None
    """
    app_call_txn = algorand_client.create_transaction.app_call(
        AppCallParams(
            sender=account_a.address,
            app_id=1234,
            on_complete=algosdk.transaction.OnComplete.NoOpOC,
        )
    )

    # example: APPLICATION_NO_OP_TRANSACTION

    # example: APPLICATION_UPDATE_TRANSACTION

    """
    Create a unsigned application update transaction updating the approval program and clear state program of an application

    Parameters for updating an application.
    - sender: The address of the account that will send the transaction
    - app_id: ID of the application
    - approval_program: The program to execute for all OnCompletes other than ClearState as raw teal (string)
        or compiled teal (bytes)
    - clear_state_program: The program to execute for ClearState OnComplete as raw teal (string)
        or compiled teal (bytes)
    """
    algorand_client.create_transaction.app_update(
        AppUpdateParams(
            sender=account_a.address,
            app_id=1234,
            approval_program=minimal_teal,
            clear_state_program=minimal_teal,
        )
    )
    # example: APPLICATION_UPDATE_TRANSACTION

    # example: APPLICATION_DELETE_TRANSACTION

    """
    Create an unsigned application delete transaction deleting an application with app id 1234

    Parameters for deleting an application.
    - sender: The address of the account that will send the transaction
    - app_id: ID of the application
    - on_complete: The OnComplete action, defaults to DeleteApplicationOC
    """
    algorand_client.create_transaction.app_delete(
        AppDeleteParams(
            sender=account_a.address,
            app_id=1234,
        )
    )
    # example: APPLICATION_DELETE_TRANSACTION

    # example: APPLICATION_OPT_IN_TRANSACTION

    """
    Create a unsigned application call transaction with the OptIn OnComplete action

    Parameters for calling an application.
    - sender: The address of the account that will send the transaction
    - on_complete: The OnComplete action
    - app_id: ID of the application, defaults to None
    """
    algorand_client.create_transaction.app_call(
        AppCallParams(
            sender=account_a.address,
            app_id=1234,
            on_complete=algosdk.transaction.OnComplete.OptInOC,
        )
    )
    # example: APPLICATION_OPT_IN_TRANSACTION

    # example: APPLICATION_CLOSE_OUT_TRANSACTION

    """
    Create a unsigned application call transaction with the CloseOut OnComplete action

    Parameters for calling an application.
    - sender: The address of the account that will send the transaction
    - on_complete: The OnComplete action
    - app_id: ID of the application, defaults to None
    """
    algorand_client.create_transaction.app_call(
        AppCallParams(
            sender=account_a.address,
            app_id=1234,
            on_complete=algosdk.transaction.OnComplete.CloseOutOC,
        )
    )
    # example: APPLICATION_CLOSE_OUT_TRANSACTION

    # example: APPLICATION_CLEAR_STATE_TRANSACTION

    """
    Create a unsigned application call transaction with the ClearState OnComplete action

    Parameters for calling an application.
    - sender: The address of the account that will send the transaction
    - on_complete: The OnComplete action
    - app_id: ID of the application, defaults to None
    """
    algorand_client.create_transaction.app_call(
        AppCallParams(
            sender=account_a.address,
            app_id=1234,
            on_complete=algosdk.transaction.OnComplete.ClearStateOC,
        )
    )
    # example: APPLICATION_CLEAR_STATE_TRANSACTION

    # example: KEY_REGISTRATION_TRANSACTION

    """
    Create an unsigned online key registration transaction

    Parameters for online key registration.
    - sender: The address of the account that will send the transaction
    - vote_key: The root participation public key
    - selection_key: The VRF public key
    - vote_first: The first round that the participation key is valid
    - vote_last: The last round that the participation key is valid
    - vote_key_dilution: The dilution for the 2-level participation key
    """
    online_key_registration_txn = (
        algorand_client.create_transaction.online_key_registration(
            OnlineKeyRegistrationParams(
                sender=account_a.address,
                vote_key="participation-public-key",
                selection_key="vrf-public-key",
                vote_first=1,
                vote_last=100,
                vote_key_dilution=1,
            )
        )
    )

    """
    Create an unsigned offline key registration transaction

    Parameters for offline key registration.
    - sender: The address of the account that will send the transaction
    - prevent_account_from_ever_participating_again: Whether to prevent the account from ever participating again
    """
    offline_key_registration_txn = (
        algorand_client.create_transaction.offline_key_registration(
            OfflineKeyRegistrationParams(
                sender=account_a.address,
                prevent_account_from_ever_participating_again=False,
            )
        )
    )

    # example: KEY_REGISTRATION_TRANSACTION


transaction_types()
