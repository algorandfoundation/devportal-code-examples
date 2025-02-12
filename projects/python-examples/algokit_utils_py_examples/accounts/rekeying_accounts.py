from algokit_utils import AlgoAmount, PaymentParams
from algokit_utils_py_examples.helpers import setup_localnet_environment


def rekeying_accounts() -> None:
    # example: REKEYING_ACCOUNT

    algorand_client, dispenser, account1, account2, _ = setup_localnet_environment()

    """
    Rekey an account to use a different address for signing.
    This allows account 1 to be controlled by account 2's private key.
    """
    algorand_client.account.rekey_account(account=account1.address, rekey_to=account2)

    payment_txn_result = algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account2.address,
            amount=AlgoAmount(algo=1),
        )
    )

    unsigned_payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account2.address,
            amount=AlgoAmount(algo=1),
            signer=account2.signer,
            first_valid_round=algorand_client.get_suggested_params().first + 1,
        )
    )

    """
    The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
    """
    result = (
        algorand_client.new_group()
        .add_transaction(transaction=unsigned_payment_txn, signer=account2.signer)
        .send()
    )

    # example: REKEYING_ACCOUNT


rekeying_accounts()
