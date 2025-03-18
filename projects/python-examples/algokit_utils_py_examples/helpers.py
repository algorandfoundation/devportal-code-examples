from algokit_utils import AlgoAmount, AlgorandClient, PaymentParams, SigningAccount


def setup_localnet_environment() -> (
    tuple[
        AlgorandClient, SigningAccount, SigningAccount, SigningAccount, SigningAccount
    ]
):
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
    accounts = [account_a, account_b, account_c]

    # Fund each test account with a small payment.
    for account in accounts:
        algorand_client.send.payment(
            PaymentParams(
                sender=dispenser.address,
                receiver=account.address,
                amount=AlgoAmount(algo=10),
            )
        )

    return (
        algorand_client,
        dispenser,
        account_a,
        account_b,
        account_c,
    )
