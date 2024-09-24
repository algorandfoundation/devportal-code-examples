from algopy import (
    Account,
    Application,
    ARC4Contract,
    Asset,
    Global,
    Txn,
    UInt64,
    arc4,
    compile_contract,
    itxn,
)
from algopy.arc4 import abimethod

from ..hello_world.contract import HelloWorld


class InnerTransactions(ARC4Contract):
    # example: PAYMENT
    @abimethod()
    def payment(self) -> UInt64:
        result = itxn.Payment(amount=5000, receiver=Txn.sender, fee=0).submit()
        return result.amount

    """
    fee is set to 0 by default. Manually set here for demonstration purposes.
    The `Sender` for the above is implied to be Global.current_application_address().

    If a different sender is needed, it'd have to be an account that has been
    rekeyed to the application address.
    """
    # example: PAYMENT

    # example: ASSET_CREATE
    @abimethod
    def asset_create(self) -> UInt64:
        itxn_result = itxn.AssetConfig(
            total=100,
            decimals=2,
            unit_name="ML",
            asset_name="Mona Lisa",
            url="https://link_to_ipfs/Mona_Lisa",
            manager=Global.current_application_address,
            reserve=Global.current_application_address,
            freeze=Global.current_application_address,
            clawback=Global.current_application_address,
            fee=0,
        ).submit()

        return itxn_result.created_asset.id

    # example: ASSET_CREATE

    # example: ASSET_OPT_IN
    @abimethod
    def asset_opt_in(self, asset: Asset) -> None:
        itxn.AssetTransfer(
            asset_receiver=Global.current_application_address,
            xfer_asset=asset,
            asset_amount=0,
            fee=0,
        ).submit()

    """
    A zero amount asset transfer to one's self is a special type of asset transfer
    that is used to opt-in to an asset.

    To send an asset transfer, the asset must be an available resource.
    Refer the Resource Availability section for more information.
    """
    # example: ASSET_OPT_IN

    # example: ASSET_TRANSFER
    @abimethod
    def asset_transfer(self, asset: Asset, receiver: Account, amount: UInt64) -> None:
        itxn.AssetTransfer(
            asset_receiver=receiver,
            xfer_asset=asset,
            asset_amount=amount,
            fee=0,
        ).submit()

    """
    For a smart contract to transfer an asset, the app account must be opted into the asset
    and be holding non zero amount of assets.

    To send an asset transfer, the asset must be an available resource.
    Refer the Resource Availability section for more information.
    """
    # example: ASSET_TRANSFER

    # example: ASSET_FREEZE
    @abimethod
    def asset_freeze(self, acct_to_be_frozen: Account, asset: Asset) -> None:
        itxn.AssetFreeze(
            freeze_account=acct_to_be_frozen,  # The account that has freeze authority on the asset.
            freeze_asset=asset,
            frozen=True,
            fee=0,
        ).submit()

    """
    To freeze an asset, the asset must be a freezable asset
    by having an account with freeze authority.
    """
    # example: ASSET_FREEZE

    # example: ASSET_REVOKE
    @abimethod
    def asset_revoke(
        self, asset: Asset, account_to_be_revoked: Account, amount: UInt64
    ) -> None:
        itxn.AssetTransfer(
            asset_receiver=Global.current_application_address,
            xfer_asset=asset,
            asset_sender=account_to_be_revoked,  # AssetSender is only used in the case of clawback
            asset_amount=amount,
            fee=0,
        ).submit()

    """
    To revoke an asset, the asset must be a revocable asset
    by having an account with clawback authority.

    Sender is implied to be current_application_address
    """
    # example: ASSET_REVOKE

    # example: ASSET_CONFIG
    @abimethod
    def asset_config(self, asset: Asset) -> None:
        itxn.AssetConfig(
            config_asset=asset,
            manager=Global.current_application_address,
            reserve=Global.current_application_address,
            freeze=Txn.sender,
            clawback=Txn.sender,
            fee=0,
        ).submit()

    """
    For a smart contract to transfer an asset, the app account must be opted into the asset
    and be holding non zero amount of assets.

    To send an asset transfer, the asset must be an available resource.
    Refer the Resource Availability section for more information.
    """
    # example: ASSET_CONFIG

    # example: ASSET_DELETE
    @abimethod
    def asset_delete(self, asset: Asset) -> None:
        itxn.AssetConfig(
            config_asset=asset,
            fee=0,
        ).submit()

    # example: ASSET_DELETE

    # example: GROUPED_INNER_TXNS
    @abimethod
    def multi_inner_txns(self, app_id: Application) -> tuple[UInt64, arc4.String]:
        payment_params = itxn.Payment(amount=5000, receiver=Txn.sender, fee=0)

        app_call_params = itxn.ApplicationCall(
            app_id=app_id,
            app_args=(arc4.arc4_signature("hello(string)string"), arc4.String("World")),
            fee=0,
        )

        pay_txn, app_call_txn = itxn.submit_txns(payment_params, app_call_params)

        hello_world_result = arc4.String.from_log(app_call_txn.last_log)
        return pay_txn.amount, hello_world_result

    # example: GROUPED_INNER_TXNS

    # example: DEPLOY_APP
    """
    HelloWorld class is a contract class defined in a different file.
    It is imported in the beginning of this file.

    from ..hello_world.contract import HelloWorld
    """

    @abimethod
    def deploy_app(self) -> UInt64:
        compiled_contract = compile_contract(HelloWorld)

        app_txn = itxn.ApplicationCall(
            approval_program=compiled_contract.approval_program,
            clear_state_program=compiled_contract.clear_state_program,
            fee=0,
        ).submit()
        app = app_txn.created_app

        return app.id

    # example: DEPLOY_APP

    # example: NOOP_APP_CALL
    @abimethod
    def noop_app_call(self, app_id: Application) -> tuple[arc4.String, arc4.String]:
        # invoke an ABI method
        call_txn = itxn.ApplicationCall(
            app_id=app_id,
            app_args=(arc4.arc4_signature("hello(string)string"), arc4.String("World")),
            fee=0,
        ).submit()
        # extract result
        first_hello_world_result = arc4.String.from_log(call_txn.last_log)

        # OR, call it automatic ARC4 encoding, type validation and result handling
        second_hello_world_result, call_txn = arc4.abi_call[
            arc4.String
        ](  # declare return type
            "hello(string)string",  # method signature to call
            "again",  # abi method arguments
            fee=0,
            app_id=app_id,
        )

        return first_hello_world_result, second_hello_world_result

    # example: NOOP_APP_CALL
