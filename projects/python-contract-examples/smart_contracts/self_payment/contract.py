from algopy import (
    Bytes,
    Global,
    TemplateVar,
    TransactionType,
    Txn,
    UInt64,
    logicsig,
    op,
)


# example: LSIG_SELFPAYMENT
@logicsig
def self_payment() -> bool:
    """
    This Delegated Account will authorize a single empty self payment in a block known ahead of time.
    """
    return (
        Txn.type_enum == TransactionType.Payment
        and Txn.receiver == Txn.sender
        and Txn.amount == 0
        and Txn.rekey_to == Global.zero_address
        and Txn.close_remainder_to == Global.zero_address
        and Txn.fee == Global.min_txn_fee
        and Global.genesis_hash == TemplateVar[Bytes]("TARGET_NETWORK_GENESIS")
        # Acquiring a lease with last_round and a non-empty lease field prevents replay attacks.
        and Txn.last_valid == TemplateVar[UInt64]("LAST_ROUND")
        and Txn.lease == op.sha256(b"self-payment")
    )


# example: LSIG_SELFPAYMENT
