from algokit_utils import AlgoAmount, MultisigMetadata, PaymentParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def multisignature_accounts() -> None:
    # example: MULTISIG_ACCOUNT

    algorand_client, dispenser, account_a, account_b, account_c = (
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
    Send a payment transaction from the multisig account
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

    # example: MULTISIG_ACCOUNT


multisignature_accounts()
