from algokit_utils import AlgoAmount, AlgorandClient


def account_code_example() -> None:
    """
    Initialize an Algorand client instance configured for LocalNet
    """
    algorand_client = AlgorandClient.default_localnet()

    # example: RANDOM_ACCOUNTS
    """
    Create random accounts that can be used for testing or development.
    Each account will have a newly generated private/public key pair.
    """
    random_account = algorand_client.account.random()
    random_account2 = algorand_client.account.random()
    random_account3 = algorand_client.account.random()
    # example: RANDOM_ACCOUNTS

    # example: ENV_ACCOUNT
    """
    Get or create an account from environment variables.
    When running against LocalNet, this will create a funded wallet
    if it doesn't exist.
    """
    env_account = algorand_client.account.from_environment(
        name="MY_ACCOUNT", fund_with=AlgoAmount(algo=1)
    )
    # example: ENV_ACCOUNT

    # example: MNEMONIC_ACCOUNT
    """
    Create an account from an existing mnemonic phrase.
    Useful for recovering accounts or using predefined test accounts.
    """
    mnemonic_account = algorand_client.account.from_mnemonic(mnemonic="MNEMONIC_PHRASE")
    # example: MNEMONIC_ACCOUNT

    # example: KMD_ACCOUNT
    """
    Get or create an account from LocalNet's KMD (Key Management Daemon)
    by name. If the account doesn't exist, it will be created.
    """
    kmd_account = algorand_client.account.from_kmd(name="ACCOUNT_NAME")
    # example: KMD_ACCOUNT

    # example: KMD_WALLET_OPERATIONS
    """
    Create a wallet with the KMD client.
    """
    algorand_client.client.kmd.create_wallet(name="ACCOUNT_NAME", pswd="password")

    """
    Rename a wallet with the KMD client.
    """
    algorand_client.client.kmd.rename_wallet(
        id="PX2KLH4IVQ25DIU2IVGDWRPJ66RJKOCJ6F7CBCBQA4IXL2GAX645WSG3IQ",
        password="new_password",
        new_name="NEW_ACCOUNT_NAME",
    )
    # example: KMD_WALLET_OPERATIONS
