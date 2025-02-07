import pytest
from algokit_utils import *
from algokit_utils.config import config

from smart_contracts.artifacts.hello_world.hello_world_client import (
    HelloArgs,
    HelloWorldClient,
    HelloWorldFactory,
)


@pytest.fixture(scope="session")
def hello_world_client(
    algorand: AlgorandClient, dispenser: SigningAccount, creator: SigningAccount
) -> HelloWorldClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        HelloWorldFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=dispenser.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


def test_says_hello(hello_world_client: HelloWorldClient) -> None:
    result = hello_world_client.send.hello(HelloArgs(name="World"))

    assert result.abi_return == "Hello, World"


def test_simulate_says_hello_with_correct_budget_consumed(
    hello_world_client: HelloWorldClient, algorand: AlgorandClient
) -> None:
    result = (
        hello_world_client.new_group()
        .hello(HelloArgs(name="World"))
        .hello(HelloArgs(name="Jane"))
        .simulate()
    )

    assert result.returns[0].value == "Hello, World"
    assert result.returns[1].value == "Hello, Jane"
    assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] < 100
