import json

from algokit_utils_py_examples.helpers import setup_localnet_environment


def fees() -> None:
    algorand_client, _, _, _, _ = setup_localnet_environment()

    # example: FEES

    """
    Get the suggested parameters for a transaction

    Returns a dict with the following attributes:
    - consensus_version: The consensus version of the network
    - fee: The fee per byte for the transaction
    - first: The first valid block round
    - flat_fee: Whether the fee is a flat fee
    - gen: The genesis name of the network
    - gh: The genesis hash of the network
    - last: The last valid block round
    - min_fee: The minimum fee for the transaction
    """

    sp = algorand_client.get_suggested_params()

    print("Minimum Fee: ", sp.min_fee)
    print("Fee: ", sp.fee)
    print("Flat Fee: ", sp.flat_fee)

    # example: FEES

    # exampleL FEE_CONFIG

    sp = algorand_client.get_suggested_params()

    sp.fee = 2000  # override the suggested fee and set it to 2000 microAlgo

    # example: FEE_CONFIG

    # Get all attributes
    sp_dict = {
        attr: getattr(sp, attr)
        for attr in dir(sp)
        if not attr.startswith("_") and not callable(getattr(sp, attr))
    }
    print(json.dumps(sp_dict, indent=2))


fees()
