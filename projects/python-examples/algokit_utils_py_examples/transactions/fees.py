import json

from algokit_utils import AlgoAmount, PaymentParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def fees() -> None:
    algorand_client, _, account_a, account_b, _ = setup_localnet_environment()

    # example: FEES

    """
    Get the suggested parameters for a transaction

    Returns a dict with the following attributes:
    - consensus_version: The consensus version of the network
    - fee: The fee per byte for the transaction
    - first: The first valid block round
    - flat_fee: Whether the fee is a flat fee
    - gen: The genesis name of the network
    - gh: The genesis hash of the network
    - last: The last valid block round
    - min_fee: The minimum fee for the transaction
    """

    sp = algorand_client.get_suggested_params()

    print("Minimum Fee: ", sp.min_fee)
    print("Fee: ", sp.fee)
    print("Flat Fee: ", sp.flat_fee)

    # example: FEES

    # exampleL FEE_CONFIG

    sp = algorand_client.get_suggested_params()

    sp.fee = 2000  # override the suggested fee and set it to 2000 microAlgo

    # example: FEE_CONFIG

    # Get all attributes
    sp_dict = {
        attr: getattr(sp, attr)
        for attr in dir(sp)
        if not attr.startswith("_") and not callable(getattr(sp, attr))
    }
    print(json.dumps(sp_dict, indent=2))

    # example: FEE_POOLING

    sp = algorand_client.get_suggested_params()

    transaction_a = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=2),
            static_fee=AlgoAmount(algo=0),  # fee is set to 0
        )
    )

    transaction_b = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
            extra_fee=max(
                sp.fee * transaction_a.estimate_size(),
                AlgoAmount(micro_algo=sp.min_fee),
            ),  # extra fee is set to the max of the suggested fee or the minimum fee to cover the fee of transaction_a
        )
    )

    """
    transaction_a and transaction_b are added to the same atomic group.
    The extra fee of transaction_b covers the fee of transaction_a.
    Therefore, the total fee sum for the group enough to cover the fee of both transactions.
    """
    result = (
        algorand_client.new_group()
        .add_transaction(transaction_a)
        .add_transaction(transaction_b)
        .send()
    )

    print(result.tx_ids)

    # example: FEE_POOLING

    # example: INNER_TXN_FEE

    sp = algorand_client.get_suggested_params()

    transaction_a = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
        )
    )

    # TODO: add inner txn example

    # example: INNER_TXN_FEE


fees()
