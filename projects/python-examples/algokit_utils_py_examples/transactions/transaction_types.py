from algokit_utils import *
from algokit_utils_py_examples.helpers import setup_localnet_environment
from smart_contracts.artifacts.hello_world.hello_world_client import (
    HelloWorldClient,
    HelloWorldFactory,
)


def transaction_types() -> None:
    # example: TRANSACTION_TYPES

    algorand_client, dispenser, account1, account2, account3 = (
        setup_localnet_environment()
    )

    # # example: PAYMENT_TRANSACTION

    # """
    # Create a unsigned payment transaction sending 1 Algo from account1 to account2
    # """
    # payment_txn = algorand_client.create_transaction.payment(
    #     PaymentParams(
    #         sender=account1.address,
    #         receiver=account2.address,
    #         amount=AlgoAmount(algo=1),
    #     )
    # )

    # """
    # Directly send a payment transaction of 2 Algo from account1 to account2 using the AlgorandClient
    # """
    # algorand_client.send.payment(
    #     PaymentParams(
    #         sender=account1.address,
    #         receiver=account2.address,
    #         amount=AlgoAmount(algo=2),
    #     )
    # )
    # # example: PAYMENT_TRANSACTION

    # # example: ASSET_TRANSFER_TRANSACTION

    # """
    # Create an unsigned asset transfer transaction of 1 asset with asset id 1234 from account1 to account2
    # """
    # asset_transfer_txn = algorand_client.create_transaction.asset_transfer(
    #     AssetTransferParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #         receiver=account2.address,
    #         amount=1,
    #     )
    # )

    # """
    # Directly send a asset transfer transaction of 1 asset with asset id 2345 from account1 to account2 using the AlgorandClient
    # """
    # algorand_client.send.asset_transfer(
    #     AssetTransferParams(
    #         sender=account1.address,
    #         asset_id=2345,
    #         receiver=account2.address,
    #         amount=1,
    #     )
    # )
    # # example: ASSET_TRANSFER_TRANSACTION

    # # example: ASSET_OPT_IN_TRANSACTION

    # """
    # Create an unsigned asset opt in transaction for account1 opting in to asset with asset id 1234
    # """
    # asset_opt_in_txn = algorand_client.create_transaction.asset_opt_in(
    #     AssetOptInParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #     )
    # )

    # """
    # Directly send a asset opt in transaction for account1 opting in to asset with asset id 2345 using the AlgorandClient
    # """
    # algorand_client.send.asset_opt_in(
    #     AssetOptInParams(
    #         sender=account1.address,
    #         asset_id=2345,
    #     )
    # )
    # # example: ASSET_OPT_IN_TRANSACTION

    # # example: ASSET_OPT_OUT_TRANSACTION

    # """
    # Create an unsigned asset opt out transaction for account1 opting out of asset with asset id 1234
    # """
    # asset_opt_out_txn = algorand_client.create_transaction.asset_opt_out(
    #     AssetOptOutParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #         creator=account2.address,
    #     )
    # )

    # """
    # Directly send a asset opt out transaction for account1 opting out of asset with asset id 2345 using the AlgorandClient
    # """
    # algorand_client.send.asset_opt_out(
    #     AssetOptOutParams(
    #         sender=account1.address,
    #         asset_id=2345,
    #         creator=account2.address,
    #     )
    # )
    # # example: ASSET_OPT_OUT_TRANSACTION

    # # example: ASSET_CREATE_TRANSACTION

    # """
    # Create an unsigned asset create transaction creating a fungible ASA with 10 million units
    # """
    # asset_create_txn = algorand_client.create_transaction.asset_create(
    #     AssetCreateParams(
    #         sender=account1.address,
    #         total=10_000_000,
    #         asset_name="My Asset",
    #         asset_unit="MYA",
    #         asset_decimals=6,
    #         asset_manager=account1.address,  # optional. Can be permanently disabled by setting to None
    #         asset_reserve=account1.address,  # optional. Can be permanently disabled by setting to None
    #         asset_freeze=account1.address,  # optional. Can be permanently disabled by setting to None
    #         asset_clawback=account1.address,  # optional. Can be permanently disabled by setting to None
    #         default_frozen=False,  # optional
    #     )
    # )

    # """
    # Directly send a asset create transaction creating a 1 to 1 unique NFT using the AlgorandClient
    # """
    # algorand_client.send.asset_create(
    #     AssetCreateParams(
    #         sender=account1.address,
    #         total=1,
    #         asset_name="My NFT",
    #         asset_unit="MNFT",
    #         asset_decimals=0,
    #         url="metadata URL",
    #         metadata_hash=b"Hash of the metadata URL",
    #     )
    # )
    # # example: ASSET_CREATE_TRANSACTION

    # # example: ASSET_CONFIG_TRANSACTION

    # """
    # Create an unsigned asset config transaction updating four mutable fields of an asset:
    # manager, reserve, freeze, clawback. This operation is only possible if the sender is
    # the asset manager and the asset has all four mutable fields set.
    # """
    # asset_config_txn = algorand_client.create_transaction.asset_config(
    #     AssetConfigParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #         manager=account3.address,
    #         reserve=account3.address,
    #         freeze=account3.address,
    #         clawback=account3.address,
    #     )
    # )

    # """
    # Directly send an asset config transaction updating the manager, reserve, freeze, clawback
    # fields of asset with asset id 2345 using the AlgorandClient
    # """
    # algorand_client.send.asset_config(
    #     AssetConfigParams(
    #         sender=account1.address,
    #         asset_id=2345,
    #         manager=account3.address,
    #         reserve=account3.address,
    #         freeze=account3.address,
    #         clawback=account3.address,
    #     )
    # )
    # # example: ASSET_CONFIG_TRANSACTION

    # # example: ASSET_FREEZE_TRANSACTION

    # """
    # Create a unsigned asset freeze transaction freezing an asset with asset id 1234
    # """
    # asset_freeze_txn = algorand_client.create_transaction.asset_freeze(
    #     AssetFreezeParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #         account=account2.address,  # The account to freeze or unfreeze
    #         frozen=True,
    #     )
    # )

    # """
    # Directly send a asset freeze transaction unfreezing an asset with asset id 1234 using the AlgorandClient
    # """
    # algorand_client.send.asset_freeze(
    #     AssetFreezeParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #         account=account2.address,  # The account to freeze or unfreeze
    #         frozen=False,
    #     )
    # )
    # # example: ASSET_FREEZE_TRANSACTION

    # # example: ASSET_DESTROY_TRANSACTION

    # """
    # Create an unsigned asset destroy transaction destroying an asset with asset id 1234
    # All of the assets must be owned by the creator of the asset before the asset can be deleted.
    # """
    # asset_destroy_txn = algorand_client.create_transaction.asset_destroy(
    #     AssetDestroyParams(
    #         sender=account1.address,
    #         asset_id=1234,
    #     )
    # )

    # """
    # Directly send a asset destroy transaction for account1 using the AlgorandClient
    # """
    # algorand_client.send.asset_destroy(
    #     AssetDestroyParams(
    #         sender=account1.address,
    #         asset_id=2345,
    #     )
    # )
    # # example: ASSET_DESTROY_TRANSACTION

    # example: APPLICATION_CREATE_TRANSACTION

    """
    Create an app factory for the hello world contract and use the facotry to deploy the contract
    """
    factory = algorand_client.client.get_typed_app_factory(
        HelloWorldFactory,
        default_sender=account1.address,
        default_signer=account1.signer,
    )

    """
    The `hello_world_client` is a typed application client that can be used to 
    interact with the deployed hello world contract
    """
    hello_world_client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    print(f"Deploy Result1: {deploy_result}")

    hello_world_client, deploy_result = factory.send.create.bare()

    print(f"Deploy Result2: {deploy_result}")

    # TODO: This is not working. Need to figure out why.
    result = algorand_client.send.app_create(
        AppCreateParams(
            sender=account1.address,
            approval_program=hello_world_client.app_spec.source.approval,
            clear_state_program=hello_world_client.app_spec.source.clear,
        )
    )

    # example: APPLICATION_CREATE_TRANSACTION

    # example: APPLICATION_NO_OP_TRANSACTION

    # """
    # Create a unsigned application call transaction calling the hello method on the hello world contract
    # """
    # app_call_txn = algorand_client.create_transaction.a.app_call(
    #     AppCallParams(
    #         sender=account1.address,
    #         app_id=1,
    #         method="hello",
    #         method_args=["Hello, World!"],
    #     )
    # )

    # """
    # Directly send a application call transaction for account1 using the AlgorandClient
    # """
    # algorand_client.send.app_call(
    #     AppCallParams(
    #         sender=account1.address,
    #         app_id=1,
    #         method="hello",
    #         method_args=["Hello, World!"],
    #     )
    # )
    # example: APPLICATION_NO_OP_TRANSACTION
    # # example: APPLICATION_UPDATE_TRANSACTION
    # # example: APPLICATION_UPDATE_TRANSACTION
    # # example: APPLICATION_DELETE_TRANSACTION
    # # example: APPLICATION_DELETE_TRANSACTION
    # # example: APPLICATION_OPT_IN_TRANSACTION
    # # example: APPLICATION_OPT_IN_TRANSACTION
    # # example: APPLICATION_CLOSE_OUT_TRANSACTION
    # # example: APPLICATION_CLOSE_OUT_TRANSACTION
    # # example: APPLICATION_CLEAR_STATE_TRANSACTION
    # # example: APPLICATION_CLEAR_STATE_TRANSACTION

    # # example: KEY_REGISTRATION_TRANSACTION

    # """
    # Create a unsigned key registration transaction for account1
    # """
    # key_registration_txn = algorand_client.create_transaction.key_registration(
    #     KeyRegistrationParams(
    #         sender=account1.address,
    #         key=account1.signer,
    #     )
    # )

    # """
    # Directly send a key registration transaction for account1 using the AlgorandClient
    # """
    # algorand_client.send.key_registration(
    #     KeyRegistrationParams(
    #         sender=account1.address,
    #         key=account1.signer,
    #     )
    # )
    # # example: KEY_REGISTRATION_TRANSACTION

    # # example: STATE_PROOF_TRANSACTION

    # """
    # Create a unsigned state proof transaction for account1
    # """
    # state_proof_txn = algorand_client.create_transaction.state_proof(
    #     StateProofParams(
    #         sender=account1.address,
    #         asset_id=1,
    #     )
    # )

    # """
    # Directly send a state proof transaction for account1 using the AlgorandClient
    # """
    # algorand_client.send.state_proof(
    #     StateProofParams(
    #         sender=account1.address,
    #         asset_id=1,
    #     )
    # )
    # example: STATE_PROOF_TRANSACTION


transaction_types()
