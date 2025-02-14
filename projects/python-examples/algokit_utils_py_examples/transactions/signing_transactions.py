import algosdk
from algokit_utils import AlgoAmount, PaymentParams, SigningAccount

from algokit_utils_py_examples.helpers import setup_localnet_environment


def signing_transactions() -> None:
    # example: SIGNING_TRANSACTIONS

    algorand_client, dispenser, account1, _, _ = setup_localnet_environment()

    """
    Transaction Signer of an account are used to sign transactions from an
    atomic transaction group.
    """
    account1_signer = account1.signer.private_key

    # Generate an account with no signer. The method returns a private key and address.
    account2_pk, account2_addr = algosdk.account.generate_account()

    # Ensure the account with no signer has enough balance
    algorand_client.account.ensure_funded(
        account_to_fund=account2_addr,
        dispenser_account=dispenser.address,
        min_spending_balance=AlgoAmount(algo=10),
    )

    # This payment transaction fails with Error: No signer found because the account has no signer
    try:
        algorand_client.send.payment(
            PaymentParams(
                sender=account2_addr,
                receiver=account1.address,
                amount=AlgoAmount(algo=1),
            )
        )
    except Exception as e:
        print(f"Error: {e}")

    """
    Tracks the given account for later signing.
    Note: If you are generating accounts via the various methods on AccountManager (like random, from_mnemonic, logic_sig, etc.)
    then they automatically get tracked.
    """
    algorand_client.account.set_signer_from_account(
        SigningAccount(private_key=account2_pk, address=account2_addr)
    )

    # Now the account is tracked and has the signer set so it can be used to sign transactions
    account_with_signer = algorand_client.account.get_account(account2_addr)

    assert account_with_signer.address == account2_addr

    # Now this payment transaction will be successful because the account has a signer
    algorand_client.send.payment(
        PaymentParams(
            sender=account2_addr,
            receiver=account1.address,
            amount=AlgoAmount(algo=1),
        )
    )

    # Set up a default signer for transactions
    # Account1 signer will be used when no specific signer is provided
    algorand_client.account.set_default_signer(account1.signer)

    # example: SIGNING_TRANSACTIONS


signing_transactions()
