from algokit_utils import AlgoAmount, AlgorandClient, MultisigMetadata, PaymentParams
from algokit_utils_py_examples.helpers import setup_localnet_environment


def multisignature_accounts() -> None:
    # example: MULTISIGNATURE_ACCOUNTS

    algorand_client, dispenser, random_account1, random_account2, random_account3 = (
        setup_localnet_environment()
    )

    """
    Create a 2-of-3 multisig account that requires
    only 2 signature from the 3 possible signers to authorize transactions
    """
    multisig_account = algorand_client.account.multisig(
        metadata=MultisigMetadata(
            version=1,
            threshold=2,
            addresses=[
                random_account1.address,
                random_account2.address,
                random_account3.address,
            ],
        ),
        signing_accounts=[random_account1, random_account2, random_account3],
    )

    algorand_client.account.ensure_funded(
        multisig_account, dispenser, AlgoAmount(algo=10)
    )

    algorand_client.send.payment(
        PaymentParams(
            sender=multisig_account.address,
            receiver=random_account1.address,
            amount=AlgoAmount(algo=1),
        ),
    )

    payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=multisig_account.address,
            receiver=random_account1.address,
            amount=AlgoAmount(algo=1),
        ),
    )

    random_account1.signer.sign_transactions()


multisignature_accounts()
