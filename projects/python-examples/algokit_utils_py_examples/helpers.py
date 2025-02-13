from algokit_utils import *


# temp
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
            - account1: The first test account.
            - account2: The second test account.
            - account3: The third test account.
    """
    # Initialize an Algorand client instance configured for LocalNet.
    algorand_client = AlgorandClient.default_localnet()

    # Retrieve the localnet dispenser account.
    dispenser = algorand_client.account.localnet_dispenser()

    # Create random accounts for testing or development.
    account1 = algorand_client.account.random()
    account2 = algorand_client.account.random()
    account3 = algorand_client.account.random()
    accounts = [account1, account2, account3]

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
        account1,
        account2,
        account3,
    )
