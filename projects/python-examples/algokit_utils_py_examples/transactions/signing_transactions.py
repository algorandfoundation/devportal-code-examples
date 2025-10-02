import algosdk
from algokit_utils import AlgoAmount, MultisigMetadata, PaymentParams, SigningAccount

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def signing_transactions() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    dispenser = env.dispenser
    account_a = env.account_a
    account_b = env.account_b
    account_c = env.account_c

    # example: TRANSACTION_WITH_NO_SIGNER

    # Generate an account with no signer. The method returns a private key and address.
    account_no_signer_pk, account_no_signer_addr = algosdk.account.generate_account()

    # Ensure the account with no signer has enough balance
    algorand_client.account.ensure_funded(
        account_to_fund=account_no_signer_addr,
        dispenser_account=dispenser.address,
        min_spending_balance=AlgoAmount(algo=10),
    )

    # This payment transaction fails with Error: No signer found because the account has no signer
    try:
        algorand_client.send.payment(
            PaymentParams(
                sender=account_no_signer_addr,
                receiver=account_a.address,
                amount=AlgoAmount(algo=1),
            )
        )
    except Exception as e:
        print(f"Error: {e}")

    """
    Track the given account for later signing.
    Note: If you are generating accounts via the various methods on AccountManager
    (like random, from_mnemonic, logic_sig, etc.) then they automatically get tracked.
    """
    algorand_client.account.set_signer_from_account(
        SigningAccount(private_key=account_no_signer_pk, address=account_no_signer_addr)
    )

    # Now the account is tracked and has the signer set so it can be used to sign transactions
    account_with_signer = algorand_client.account.get_account(account_no_signer_addr)

    assert account_with_signer.address == account_no_signer_addr

    algorand_client.send.payment(
        PaymentParams(
            sender=account_with_signer.address,
            receiver=account_a.address,
            amount=AlgoAmount(algo=1),
        )
    )

    # example: TRANSACTION_WITH_NO_SIGNER

    # example: TRANSACTION_WITH_SIGNER

    """
    When working with `SigningAccount` account type, it includes a signer that can be used to sign transactions.
    There are two ways to sign transactions using the Algorand Client.
    """
    account_a_signer = account_a.signer

    """
    Method 1: Create an unsigned transaction and sign it with the `signer` attribute of the `SigningAccount` object.
    """
    unsigned_pay_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
        )
    )

    algorand_client.new_group().add_transaction(
        transaction=unsigned_pay_txn, signer=account_a.signer
    ).send()

    """
    Method 2: Directly send the transaction using the `send` property of the Algorand Client and pass in the signer.
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=account_b.address,
            receiver=account_a.address,
            amount=AlgoAmount(algo=1),
            signer=account_b.signer,
        )
    )

    """
    You can also set a default signer for the Algorand client.
    The default signer, which is now account_a, will be used when no specific signer is provided.
    """
    algorand_client.account.set_default_signer(account_a.signer)

    # The Algorand Client now knows the default signer and you do not need to pass in the signer.
    algorand_client.send.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
        )
    )
    # example: TRANSACTION_WITH_SIGNER

    # example: MULTISIG_SIGNING_TRANSACTIONS

    """
    Create a 2-of-3 multisig account that requires
    only 2 signature from the 3 possible signers to authorize transactions
    """
    multisig_account = algorand_client.account.multisig(
        metadata=MultisigMetadata(
            version=1,
            threshold=2,
            addresses=[
                account_a.address,
                account_b.address,
                account_c.address,
            ],
        ),
        signing_accounts=[account_a, account_b, account_c],
    )

    algorand_client.account.ensure_funded(
        multisig_account.address, dispenser, AlgoAmount(algo=10)
    )

    """
    Method 1: Create an unsigned transaction from the multisig account and sign it
    with the `signer` attribute of the `SigningAccount` object.
    """
    unsigned_pay_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=multisig_account.address,
            receiver=account_a.address,
            amount=AlgoAmount(algo=1),
        ),
    )

    algorand_client.new_group().add_transaction(
        transaction=unsigned_pay_txn, signer=multisig_account.signer
    ).send()

    """
    Method 2: Send a payment transaction from the multisig account
    which will automatically collect the required number of signatures
    from the signing accounts provided when creating the multisig account
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=multisig_account.address,
            receiver=account_a.address,
            amount=AlgoAmount(algo=1),
        ),
    )

    # example: MULTISIG_SIGNING_TRANSACTIONS


signing_transactions()
