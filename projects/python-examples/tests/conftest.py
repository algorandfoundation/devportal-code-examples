import pytest
from algokit_utils import AlgoAmount, AlgorandClient, PaymentParams, SigningAccount


@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Get an AlgorandClient to use throughout the tests"""
    algorand = AlgorandClient.default_localnet()
    algorand.set_default_validity_window(1000)

    return algorand


@pytest.fixture(scope="session")
def dispenser(algorand: AlgorandClient) -> SigningAccount:
    """Get the dispenser to fund test addresses"""
    return algorand.account.localnet_dispenser()


@pytest.fixture(scope="session")
def creator(algorand: AlgorandClient, dispenser: SigningAccount) -> SigningAccount:
    """Get an account to use as the creator of the contract"""
    acct = algorand.account.random()

    # Make sure the account has some ALGO
    algorand.send.payment(
        PaymentParams(
            sender=dispenser.address, receiver=acct.address, amount=AlgoAmount(algo=100)
        )
    )

    return acct


@pytest.fixture(scope="session")
def alice(algorand: AlgorandClient, dispenser: SigningAccount) -> SigningAccount:
    """Get an account to use as Alice who will participate in the auction"""
    acct = algorand.account.random()

    # Make sure the account has some ALGO
    algorand.send.payment(
        PaymentParams(
            sender=dispenser.address, receiver=acct.address, amount=AlgoAmount(algo=100)
        )
    )

    return acct
