from algokit_utils import (
    AlgoAmount,
    AlgoClientNetworkConfig,
    AlgorandClient,
    PaymentParams,
)

from algokit_utils_py_examples.helpers import setup_localnet_environment


def algorand_client_bootstrap() -> None:
    algorand_client, _, account_a, account_b, _ = setup_localnet_environment()

    algod = algorand_client.client.algod
    indexer = algorand_client.client.indexer
    kmd = algorand_client.client.kmd

    algod_config = AlgoClientNetworkConfig(server="http://localhost", token="4001")
    indexer_config = AlgoClientNetworkConfig(server="http://localhost", token="4001")
    kmd_config = AlgoClientNetworkConfig(server="http://localhost", token="4001")

    # example: INSTANTIATE_ALGORAND_CLIENT
    # Point to the network configured through environment variables or
    #  if no environment variables it will point to the default LocalNet
    #  configuration
    algorand_client = AlgorandClient.from_environment()
    # Point to default LocalNet configuration
    algorand_client = AlgorandClient.default_localnet()
    # Point to TestNet using AlgoNode free tier
    algorand_client = AlgorandClient.testnet()
    # Point to MainNet using AlgoNode free tier
    algorand_client = AlgorandClient.mainnet()
    # Point to a pre-created algod client
    algorand_client = AlgorandClient.from_clients(algod)
    # Point to pre-created algod, indexer and kmd clients
    algorand_client = AlgorandClient.from_clients(algod, indexer, kmd)
    # Point to custom configuration for algod
    algorand_client = AlgorandClient.from_config(
        AlgoClientNetworkConfig(
            server="http://localhost",
            token="4001",
        )
    )
    # Point to custom configuration for algod, indexer and kmd
    algorand_client = AlgorandClient.from_config(
        algod_config, indexer_config, kmd_config
    )
    # example: INSTANTIATE_ALGORAND_CLIENT

    # example: SDK_CLIENTS

    algod = algorand_client.client.algod
    indexer = algorand_client.client.indexer
    kmd = algorand_client.client.kmd

    # example: SDK_CLIENTS

    # example: TXN_WITHOUT_SIGNER_CACHE

    """
    If you don't want the Algorand client to cache the signer,
    you can manually provide the signer.
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
            signer=account_a.signer,  # The signer must be manually provided
        )
    )
    # example: TXN_WITHOUT_SIGNER_CACHE

    # example: SIGNER_CONFIG

    """
    By setting signers of accounts to the algorand client, the client will cache the signers
    and use them to sign transactions when the sender is one of the accounts.
    """

    # If no signer is provided, the client will use the default signer
    algorand_client.set_default_signer(account_a.signer)

    # If you have an address and a signer, use this method to set the signer
    algorand_client.set_signer(account_a.address, account_a.signer)

    # If you have a `SigningAccount` object, use this method to set the signer
    algorand_client.set_signer_from_account(account_a)

    """
    The Algorand client can directly send this payment transaction without
    needing a signer because it is tracking the signer for account_a.
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
        )
    )
    # example: SIGNER_CONFIG

    # example: SUGGESTED_PARAMS_CONFIG

    """
    Sets the default validity window for transactions.

    :param validity_window: The number of rounds between the first and last valid rounds
    :return: The `AlgorandClient` so method calls can be chained
    """
    algorand_client.set_default_validity_window(1000)

    """
    Get suggested params for a transaction (either cached or from algod if the cache is stale or empty)
    """
    sp = algorand_client.get_suggested_params()

    # The suggested params can be modified like below
    sp.flat_fee = True
    sp.fee = 2000

    """
    Sets a cache value to use for suggested params. Use this method to use modified suggested params for
    the next transaction.

    :param suggested_params: The suggested params to use
    :param until: A timestamp until which to cache, or if not specified then the timeout is used
    :return: The `AlgorandClient` so method calls can be chained
    """
    algorand_client.set_suggested_params_cache(sp)

    """
    Sets the timeout for caching suggested params. If set to 0, the Algorand client
    will request suggested params from the algod client every time.

    :param timeout: The timeout in milliseconds
    :return: The `AlgorandClient` so method calls can be chained
    """
    algorand_client.set_suggested_params_cache_timeout(0)
    # example: SUGGESTED_PARAMS_CONFIG


def app_client() -> None:
    algorand_client, _, account_a, account_b, _ = setup_localnet_environment()

    # example: GET_APP_CLIENT_WHEN_DEPLOYED
    from smart_contracts.artifacts.hello_world.hello_world_client import (
        HelloArgs,
        HelloWorldClient,
        HelloWorldFactory,
    )

    """
    Get a single typed app client by id
    """
    app_client = algorand_client.client.get_typed_app_client_by_id(
        HelloWorldClient,
        app_id=1234,
    )
    # or
    app_client = HelloWorldClient(
        algorand=algorand_client,
        app_id=1234,
    )

    """
    For multiple app client instances use the factory
    """
    factory = algorand_client.client.get_typed_app_factory(HelloWorldFactory)
    # or
    factory = HelloWorldFactory(algorand_client)

    app_client1 = factory.get_app_client_by_id(
        app_id=1234,
    )
    app_client2 = factory.get_app_client_by_id(
        app_id=4321,
    )

    """
    Get typed app client by creator and name
    """
    app_client = algorand_client.client.get_typed_app_client_by_creator_and_name(
        HelloWorldClient,
        creator_address=account_a.address,
        app_name="contract-name",
        # ...
    )
    # or
    app_client = HelloWorldClient.from_creator_and_name(
        algorand=algorand_client,
        creator_address=account_a.address,
        app_name="contract-name",
        # ...
    )

    """
    For multiple app client instances use the factory
    """
    factory = algorand_client.client.get_typed_app_factory(HelloWorldFactory)
    # or
    factory = HelloWorldFactory(algorand_client)

    app_client1 = factory.get_app_client_by_creator_and_name(
        creator_address="CREATORADDRESS",
        app_name="contract-name",
        # ...
    )
    app_client2 = factory.get_app_client_by_creator_and_name(
        creator_address="CREATORADDRESS",
        app_name="contract-name-2",
        # ...
    )

    # example: GET_APP_CLIENT_WHEN_DEPLOYED

    # example: APP_NOT_DEPLOYED_APP_CREATE
    from smart_contracts.artifacts.custom_create.custom_create_client import (
        CustomCreateArgs,
        CustomCreateFactory,
    )

    """
    Deploy a New App
    """
    factory = algorand_client.client.get_typed_app_factory(HelloWorldFactory)
    # or
    factory = HelloWorldFactory(algorand_client)

    app_client, create_response = factory.send.create.bare()

    # or if the contract has a custom create method:
    factory2 = algorand_client.client.get_typed_app_factory(CustomCreateFactory)

    custom_create_app_client, factory_create_response = (
        factory2.send.create.custom_create(CustomCreateArgs(age=28))
    )

    """
    Deploy or Resolve App Idempotently by Creator and Name
    """
    app_client, deploy_response = factory.deploy(
        app_name="contract-name",
    )
    # example: APP_NOT_DEPLOYED_APP_CREATE

    # example: APP_CLIENT_CALL_METHOD
    response = app_client.send.hello(args=HelloArgs(name="world"))
    print(response.abi_return)

    # example: APP_CLIENT_CALL_METHOD

    # example: FULL_APP_CLIENT_EXAMPLE
    # A similar working example can be seen in the AlgoKit init production smart contract templates, when using Python deployment
    # In this case the generated factory is called `HelloWorldAppFactory` and is in `./artifacts/HelloWorldApp/client.py`
    from algokit_utils import AlgorandClient

    from smart_contracts.artifacts.hello_world.hello_world_client import (
        HelloArgs,
        HelloWorldClient,
        HelloWorldFactory,
    )

    # These require environment variables to be present, or it will retrieve from default LocalNet
    algorand = AlgorandClient.from_environment()
    deployer = algorand.account.from_environment("DEPLOYER", AlgoAmount.from_algo(1))

    # Create the typed app factory
    factory = algorand.client.get_typed_app_factory(
        HelloWorldFactory,
        default_sender=deployer.address,
    )

    # Create the app and get a typed app client for the created app (note: this creates a new instance of the app every time,
    #  you can use .deploy() to deploy idempotently if the app wasn't previously
    #  deployed or needs to be updated if that's allowed)
    app_client, create_response = factory.send.create.bare()

    # Make a call to an ABI method and print the result
    response = app_client.send.hello(args=HelloArgs(name="world"))
    print(response.abi_return)
    # example: FULL_APP_CLIENT_EXAMPLE
