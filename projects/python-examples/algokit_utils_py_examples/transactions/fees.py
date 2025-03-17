import json

from algokit_utils import (
    AlgoAmount,
    CommonAppCallParams,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SendParams,
)

from algokit_utils_py_examples.helpers import setup_localnet_environment
from smart_contracts.artifacts.inner_transactions.inner_transactions_client import (
    InnerTransactionsFactory,
)


def fees() -> None:
    algorand_client, localnet_dispenser, account_a, account_b, _ = (
        setup_localnet_environment()
    )

    # example: SUGGESTED_PARAMS

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

    # example: SUGGESTED_PARAMS

    # Get all attributes
    sp_dict = {
        attr: getattr(sp, attr)
        for attr in dir(sp)
        if not attr.startswith("_") and not callable(getattr(sp, attr))
    }
    print(json.dumps(sp_dict, indent=2))

    # example: MAX_FEE

    """
    The Algorand client automatically gets the suggested parameters and cache them.
    This transaction will use the suggested fee from algod and it will fluctuate when
    the network is congested. Ensure to set a max fee to avoid paying more than expected.
    """
    algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
            max_fee=AlgoAmount(
                micro_algo=sp.min_fee * 3
            ),  # set the max fee to 3 times the minimum fee
        )
    )
    # example: MAX_FEE

    # example: FLAT_FEE
    """
    Set a static fee to the transaction.
    This transaction will use 2000 microAlgo no matter the network conditions
    and may fail if the network is congested.
    """
    algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
            static_fee=AlgoAmount(micro_algo=2000),  # set the fee to 2000 microAlgo
        )
    )

    """
    Or get the suggested parameters and directly configure the flat fee to true
    and set the fee to 2000 microAlgo.
    """
    sp = algorand_client.get_suggested_params()

    sp.flat_fee = True
    sp.fee = 2000

    # Cache the configured suggested parameters and use it for future transactions
    algorand_client.set_suggested_params(sp)

    # example: FLAT_FEE

    # example: FEE_POOLING

    # Transaction A will not pay any fees
    transaction_a = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=2),
            static_fee=AlgoAmount(algo=0),  # fee is set to 0
        )
    )

    # Transaction B has the `extra_fee` field set to cover the fee of transaction_a
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

    factory = algorand_client.client.get_typed_app_factory(
        InnerTransactionsFactory,
        default_sender=account_a.address,
        default_signer=account_a.signer,
    )

    app_client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand_client.account.ensure_funded(
        account_to_fund=app_client.app_address,
        dispenser_account=localnet_dispenser,
        min_spending_balance=AlgoAmount(algo=1),
    )

    """
    By setting `cover_app_call_inner_transaction_fees` to true, this transaction will
    pay extra fees to cover the fees for any inner transactions in the contract method.
    """
    app_client.send.payment(
        send_params=SendParams(cover_app_call_inner_transaction_fees=True)
    )

    """
    You can also set the `extra_fee` in the `CommonAppCallParams` to cover the fees for
    one inner transaction in the contract method. This would fail if the contract method
    has more than one inner transaction.
    """
    app_client.send.payment(
        params=CommonAppCallParams(extra_fee=AlgoAmount(micro_algo=1000))
    )

    # example: INNER_TXN_FEE


fees()
