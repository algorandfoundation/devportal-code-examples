import pytest
from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    CommonAppCallParams,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SigningAccount,
)
from algokit_utils.config import config

from smart_contracts.artifacts.arc4_types.arc4_dynamic_array_client import (
    Arc4DynamicArrayClient,
    Arc4DynamicArrayFactory,
    HelloArgs,
)
from smart_contracts.artifacts.arc4_types.arc4_static_array_client import (
    Arc4StaticArrayClient,
    Arc4StaticArrayFactory,
)
from smart_contracts.artifacts.arc4_types.arc4_struct_client import (
    AddTodoArgs,
    Arc4StructClient,
    Arc4StructFactory,
    CompleteTodoArgs,
    ReturnTodoArgs,
)
from smart_contracts.artifacts.arc4_types.arc4_tuple_client import (
    AddContactInfoArgs,
    Arc4TupleClient,
    Arc4TupleFactory,
)
from smart_contracts.artifacts.arc4_types.arc4_types_client import (
    AddArc4BiguintNArgs,
    AddArc4Uint64Args,
    AddArc4UintNArgs,
    Arc4AddressPropertiesArgs,
    Arc4AddressReturnArgs,
    Arc4ByteArgs,
    Arc4TypesClient,
    Arc4TypesFactory,
)


@pytest.fixture(scope="session")
def arc4_statc_array_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> Arc4StaticArrayClient:
    """Deploy the arc4 static array App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        Arc4StaticArrayFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def arc4_dynamic_array_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> Arc4DynamicArrayClient:
    """Deploy the arc4 static array App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        Arc4DynamicArrayFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def arc4_tuple_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> Arc4TupleClient:
    """Deploy the arc4 static array App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        Arc4TupleFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def arc4_struct_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> Arc4StructClient:
    """Deploy the arc4 struct App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        Arc4StructFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


@pytest.fixture(scope="session")
def arc4_types_app_client(
    creator: SigningAccount, algorand: AlgorandClient
) -> Arc4TypesClient:
    """Deploy the arc4 types App and create an app client the creator will use to interact with the contract"""

    config.configure(
        debug=True,
        # trace_all=True,
    )

    factory = algorand.client.get_typed_app_factory(
        Arc4TypesFactory,
        default_sender=creator.address,
        default_signer=creator.signer,
    )

    client, deploy_result = factory.deploy(
        on_update=OnUpdate.ReplaceApp,
        on_schema_break=OnSchemaBreak.Fail,
    )

    algorand.send.payment(
        PaymentParams(
            sender=creator.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=1),  # 1 Algo
        )
    )

    return client


def test_arc4_uint64(
    arc4_types_app_client: Arc4TypesClient,
) -> None:
    """Test the arc4_uint64 method"""

    # Call the arc4_uint64 method
    result = arc4_types_app_client.send.add_arc4_uint64(
        args=AddArc4Uint64Args(a=1, b=2)
    )

    # Check the result
    assert result.abi_return == 3


def test_arc4_uint_n(
    arc4_types_app_client: Arc4TypesClient,
) -> None:
    """Test the arc4_uint_n method"""

    result = arc4_types_app_client.send.add_arc4_uint_n(
        args=AddArc4UintNArgs(a=100, b=1_000, c=100_000, d=100_000)
    )

    assert result.abi_return == 201_100


def test_arc4_biguint_n(
    arc4_types_app_client: Arc4TypesClient,
) -> None:
    """Test the arc4_uint_n method"""

    result = arc4_types_app_client.send.add_arc4_biguint_n(
        args=AddArc4BiguintNArgs(a=2**65, b=2**129, c=2**257)
    )

    assert result.abi_return == 2**65 + 2**129 + 2**257


def test_arc4_byte(
    arc4_types_app_client: Arc4TypesClient,
) -> None:
    """Test the arc4_byte method"""

    result = arc4_types_app_client.send.arc4_byte(Arc4ByteArgs(a=5))

    assert result.abi_return == 6


def test_arc4_address_properties(
    arc4_types_app_client: Arc4TypesClient,
    creator: SigningAccount,
    algorand: AlgorandClient,
) -> None:
    """Test the arc4_address_properties method"""

    # Call the arc4_address method
    result = arc4_types_app_client.send.arc4_address_properties(
        Arc4AddressPropertiesArgs(address=creator.address)
    )

    creator_info = algorand.account.get_information(creator.address)

    assert result.abi_return == creator_info.amount


def test_arc4_address_return(
    arc4_types_app_client: Arc4TypesClient, creator: SigningAccount
) -> None:
    """Test the arc4_address_return method"""

    # Call the arc4_address method
    result = arc4_types_app_client.send.arc4_address_return(
        Arc4AddressReturnArgs(address=creator.address)
    )

    # Check the result
    assert result.abi_return == creator.address


def test_arc4_static_array(arc4_statc_array_app_client: Arc4StaticArrayClient) -> None:
    """Test the arc4_static_array method"""

    # Call the arc4_static_array method
    result = arc4_statc_array_app_client.send.arc4_static_array()

    assert result.abi_return is None


def test_arc4_dynamic_array(
    arc4_dynamic_array_app_client: Arc4DynamicArrayClient,
) -> None:
    """Test the arc4_dynamic_array method"""

    # Call the arc4_static_array method with simulate to avoid opcode budget constraints.
    result = (
        arc4_dynamic_array_app_client.new_group()
        .hello(HelloArgs(name="John"))
        .simulate(extra_opcode_budget=700)
    )

    assert result.returns[0].value == "Hello John!"


def test_arc4_dynamic_bytes(
    arc4_dynamic_array_app_client: Arc4DynamicArrayClient,
) -> None:
    """Test the arc4_dynamic_bytes method"""

    # Call the arc4_static_array method.
    result = arc4_dynamic_array_app_client.send.arc4_dynamic_bytes()

    assert result.abi_return is not None
    assert result.abi_return == [0, 255, 255, 170, 187, 255]  # type: ignore[comparison-overlap]


def test_arc4_struct_add_todo(arc4_struct_app_client: Arc4StructClient) -> None:
    """Test the add_todo method"""

    # Call the add_todo method
    result = arc4_struct_app_client.send.add_todo(AddTodoArgs(task="wash the dishes"))

    assert result.abi_return is not None, "Expected ABI return for add_todo"
    assert result.abi_return[0][0] == "wash the dishes"
    assert result.abi_return[0][1] is False
    assert len(result.abi_return) == 1


def test_arc4_struct_complete_and_return_todo(
    arc4_struct_app_client: Arc4StructClient,
    algorand: AlgorandClient,
) -> None:
    """Test the complete_todo method"""

    # Call the add_todo method
    arc4_struct_app_client.send.add_todo(AddTodoArgs(task="walk my dogs"))

    result = arc4_struct_app_client.send.return_todo(
        ReturnTodoArgs(task="walk my dogs")
    )

    # Check the result using tuple indexing (i.e. [0] for task and [1] for completion flag)
    assert result.abi_return is not None, "Expected ABI return for return_todo"
    assert result.abi_return.task == "walk my dogs"
    assert result.abi_return.completed is False

    # Call the complete_todo method
    arc4_struct_app_client.send.complete_todo(CompleteTodoArgs(task="walk my dogs"))
    # print("todo_result", result)

    result = arc4_struct_app_client.send.return_todo(
        ReturnTodoArgs(task="walk my dogs"),
        params=CommonAppCallParams(
            first_valid_round=algorand.get_suggested_params().first + 1
        ),
    )

    # Check the result for the completed todo using tuple indexing
    assert result.abi_return is not None, "Expected ABI return for completed todo"
    assert result.abi_return.task == "walk my dogs"
    assert result.abi_return.completed is True


def test_tuple_add_contact_info(
    arc4_tuple_app_client: Arc4TupleClient,
) -> None:
    """Test the add_contact_info method"""

    result = arc4_tuple_app_client.send.add_contact_info(
        AddContactInfoArgs(contact=("Alice", "alice@something.com", 555_555_555))
    )

    assert result.abi_return == 555_555_555


def test_tuple_return_contact(
    arc4_tuple_app_client: Arc4TupleClient,
) -> None:
    """Test the return_contact method"""

    result = arc4_tuple_app_client.send.return_contact()

    assert result.abi_return is not None, "Expected ABI return for return_contact"
    assert result.abi_return == ["Alice", "alice@something.com", 555_555_555]  # type: ignore[comparison-overlap]
