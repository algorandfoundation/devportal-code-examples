import json

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def blocks() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client

    # example: BLOCKS
    """
    Get the block for the given round.

    Args:
    block (int): block number
    response_format (str): the format in which the response is returned: either "json" or "msgpack"
    round_num (int, optional): alias for block; specify one of these
    """
    block = algorand_client.client.algod.block_info(1)

    # Pretty print the block information using JSON
    print(json.dumps(block, indent=2, sort_keys=True))
    """
    {
        "block": {
            "bi": 10000000,
            "fc": 1000,
            "fees": "A7NMWS3NT3IUDMLVO26ULGXGIIOUQ3ND2TXSER6EBGRZNOBOUIQXHIBGDE",
            "gen": "dockernet-v1",
            "gh": "pTy7N0gJNkH5YPyoWuLt9Bm+P/VI5BVTGYrLJKv6pA8=",
            "prev": "blk-YIJV66JRHWW64FW57YG74RJ3WVJS2KIA3IWPZLEQJDBH7G4TO4WQ",
            "proto": "https://github.com/algorandfoundation/specs/tree/236dcc18c9c507d794813ab768e467ea42d1b4d9",
            "rnd": 1,
            "rwcalr": 500000,
            "rwd": "7777777777777777777777777777777777777777777777777774MSJUVU",
            "seed": "whNfeTE9re4W3f4N/kU7tVMtKQDaLPyskEjCf5uTdy0=",
            "spt": {
                "0": {
                    "n": 512
                }
            },
            "tc": 1001,
            "ts": 1742832892,
            "txn": "ClBQfSWE6Ox1gU9ziKlDg0ZBy8PIaMsRx/Nft10dIak=",
            "txn256": "xWwLqxRYTXXn7msOFz9REHU8NdnMl2lW/AYt9otWS2w=",
            "txns": [
                {
                    "hgi": true,
                    "sig": "alcTaUa5xCHShxaIh0jzqwIJfQC0CvJ2Cd2iaN5rKLk4mT+GJ5Wee5YxtcL0jvUxXuvfXaWqaJmI3ru1miquBg==",
                    "txn": {
                        "amt": 1000000000,
                        "fee": 1000,
                        "lv": 1000,
                        "rcv": "4YT6S2W3BLHF3HCTG4S6GDOJOIO3BXZVYHPYSVNTN5ZB3RUWL4GDDBN4JI",
                        "snd": "HUKNKLFL6VUFLFQQUT3STTNXEFSHHKZMF7IODY57CH2OGWQTBXCMUIFVMY",
                        "type": "pay"
                    }
                }
            ]
        }
    }
    """
    # example: BLOCKS


blocks()
