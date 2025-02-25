from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    PaymentParams,
)


def funding_accounts() -> None:
    """
    Initialize an Algorand client instance configured for LocalNet
    """
    algorand_client = AlgorandClient.default_localnet()

    """
    Create random accounts that can be used for testing or development.
    Each account will have a newly generated private/public key pair.
    """
    random_account = algorand_client.account.random()

    # example: LOCALNET_DISPENSER
    """
    Returns the default LocalNet dispenser account.
    This account can be used to fund test accounts on LocalNet.
    """
    localnet_dispenser = algorand_client.account.localnet_dispenser()
    # example: LOCALNET_DISPENSER

    # example: DISPENSER_ACCOUNT
    """
    Returns an account (with private key loaded) that can act as a dispenser from environment variables.
    If environment variables are not present, returns the default LocalNet dispenser account.
    """
    dispenser = algorand_client.account.dispenser_from_environment()
    # example: DISPENSER_ACCOUNT

    """
    Send a payment from the dispenser account to the random account.
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=localnet_dispenser.address,
            receiver=random_account.address,
            amount=AlgoAmount(algo=10),
        )
    )

    # example: ENSURE_FUNDED
    """
    Funds a given account using a dispenser account as a funding source.
    Ensures the given account has a certain amount of Algo free to spend (accounting for Algo locked in minimum balance requirement).
    """
    algorand_client.account.ensure_funded(
        account_to_fund=random_account.address,
        dispenser_account=localnet_dispenser.address,
        min_spending_balance=AlgoAmount(algo=10),
    )
    # example: ENSURE_FUNDED

    # example: ENSURE_FUNDED_FROM_ENV
    """
    Ensure an account is funded from a dispenser account configured in environment.
    Uses a dispenser account retrieved from the environment, per the dispenser_from_environment method, as a funding source such that the given account has a certain amount of Algo free to spend (accounting for Algo locked in minimum balance requirement).
    """
    algorand_client.account.ensure_funded_from_environment(
        account_to_fund=random_account.address,
        min_spending_balance=AlgoAmount(algo=10),
    )
    # example: ENSURE_FUNDED_FROM_ENV
    
    # example: ENSURE_FUNDED_TESTNET
    """
    Ensure an account is funded from a dispenser account retrieved from the testnet dispenser API.
    Uses a dispenser account retrieved from the testnet dispenser API, per the ensure_funded_from_testnet_dispenser_api method, as a funding source such that the given account has a certain amount of Algo free to spend (accounting for Algo locked in minimum balance requirement).
    """
    testnet_dispenser = algorand_client.client.get_testnet_dispenser()

    algorand_client.account.ensure_funded_from_testnet_dispenser_api(
        account_to_fund=random_account.address,
        dispenser_client=testnet_dispenser,
        min_spending_balance=AlgoAmount(algo=10),
    )
    # example: ENSURE_FUNDED_TESTNET

    # example: TESTNET_DISPENSER_FUND
    """
    Directly fund an account using the TestNet Dispenser API
    """
    testnet_dispenser = algorand_client.client.get_testnet_dispenser()
    testnet_dispenser.fund(address=random_account.address, amount=10, asset_id=0)
    # example: TESTNET_DISPENSER_FUND
