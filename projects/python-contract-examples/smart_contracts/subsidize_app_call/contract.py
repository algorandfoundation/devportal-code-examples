from algopy import (
    Application,
    Bytes,
    Global,
    TemplateVar,
    TransactionType,
    Txn,
    UInt64,
    logicsig,
)
from algopy.op import GTxn


# example: LSIG_SUBSIDIZEAPPCALL
@logicsig
def subsidize_app_call() -> bool:
    """
    This Contract Account will subsidize the fees for any AppCall transaction directed to a known application.
    """
    return (
        # is it safe to pay for the fees of the previous transaction?
        Txn.type_enum == TransactionType.Payment
        and Txn.receiver == Txn.sender
        and Txn.amount == 0
        and Txn.rekey_to == Global.zero_address
        and Txn.close_remainder_to == Global.zero_address
        and Txn.fee == 2 * Global.min_txn_fee
        and Txn.last_valid <= TemplateVar[UInt64]("EXPIRATION_ROUND")
        and Global.genesis_hash == TemplateVar[Bytes]("TARGET_NETWORK_GENESIS")
        # is the previous transaction in the group an application call to a known app?
        and GTxn.type_enum(Txn.group_index - 1) == TransactionType.ApplicationCall
        and GTxn.application_id(Txn.group_index - 1)
        == TemplateVar[Application]("KNOWN_APP")
        and GTxn.fee(Txn.group_index - 1) == 0
    )


# example: LSIG_SUBSIDIZEAPPCALL
