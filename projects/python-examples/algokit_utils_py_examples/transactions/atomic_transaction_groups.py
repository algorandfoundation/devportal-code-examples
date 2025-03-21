from algokit_utils import AlgoAmount, PaymentParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def atomic_transaction_groups() -> None:
    algorand_client, dispenser, account_a, account_b, account_c = (
        setup_localnet_environment()
    )

    # example: ATOMIC_TRANSACTION_GROUP
    """
    Create a transaction group that will execute atomically
    Either all transactions succeed, or they all fail
    """
    algorand_client.new_group().add_payment(  # First transaction: Payment from A to B
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
            note=b"First payment in atomic group",
        )
    ).add_payment(  # Second transaction: Payment from B to C
        PaymentParams(
            sender=account_b.address,
            receiver=account_c.address,
            amount=AlgoAmount(
                micro_algo=500_000
            ),  # B sends half of what they received to C
            note=b"Second payment in atomic group",
        )
    ).send()  # Send the atomic group of transactions
    # example: ATOMIC_TRANSACTION_GROUP

    # example: ATOMIC_GROUP_SIMULATE
    """
    Create a transaction group to simulate
    Simulation allows you to test the transaction without committing it to the chain
    """
    group = (
        algorand_client.new_group()
        .add_payment(
            PaymentParams(
                sender=account_a.address,
                receiver=account_b.address,
                amount=AlgoAmount(algo=1),
            )
        )
        .add_payment(
            PaymentParams(
                sender=account_b.address,
                receiver=account_c.address,
                amount=AlgoAmount(micro_algo=500_000),
            )
        )
    )

    """
    Simulate the transaction group to:
    - Verify it will succeed
    - Understand its effects
    - Get execution costs
    - Debug any issues
    """
    simulate_result = group.simulate()
    assert simulate_result.simulate_response is not None

    txn_group = simulate_result.simulate_response["txn-groups"][0]

    print(
        "Simulation results:",
        {
            "round": simulate_result.simulate_response["last-round"],
            "success": not txn_group["txn-results"][0]["txn-result"]["pool-error"],
            "error": txn_group["txn-results"][0]["txn-result"]["pool-error"] or "None",
        },
    )

    # If simulation succeeds, send the actual transaction
    group.send()

    # example: ATOMIC_GROUP_SIMULATE


atomic_transaction_groups()
