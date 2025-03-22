# flake8: noqa
# fmt: off
# mypy: ignore-errors
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^3.0.0

# common
import dataclasses
import typing
# core algosdk
import algosdk
from algosdk.transaction import OnComplete
from algosdk.atomic_transaction_composer import TransactionSigner
from algosdk.source_map import SourceMap
from algosdk.transaction import Transaction
from algosdk.v2client.models import SimulateTraceConfig
# utils
import algokit_utils
from algokit_utils import AlgorandClient as _AlgoKitAlgorandClient

_APP_SPEC_JSON = r"""{"arcs": [22, 28], "bareActions": {"call": [], "create": []}, "methods": [{"actions": {"call": [], "create": ["NoOp"]}, "args": [{"type": "uint64", "name": "age"}], "name": "custom_create", "returns": {"type": "void"}, "events": [], "readonly": false, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [], "name": "get_age", "returns": {"type": "uint64"}, "events": [], "readonly": false, "recommendations": {}}], "name": "CustomCreate", "state": {"keys": {"box": {}, "global": {"age": {"key": "YWdl", "keyType": "AVMString", "valueType": "AVMUint64"}}, "local": {}}, "maps": {"box": {}, "global": {}, "local": {}}, "schema": {"global": {"bytes": 0, "ints": 1}, "local": {"bytes": 0, "ints": 0}}}, "structs": {}, "byteCode": {"approval": "CiACAAEmAQNhZ2UxG0EAFYICBEgzMe4EViezzTYaAI4CABgAAiJDMRkURDEYRIgAJRaABBUffHVMULAjQzEZFEQxGBRENhoBF4gAAiNDigEAKIv/Z4kiKGVEiQ==", "clear": "CoEBQw=="}, "compilerInfo": {"compiler": "puya", "compilerVersion": {"major": 4, "minor": 5, "patch": 2}}, "events": [], "networks": {}, "source": {"approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBzbWFydF9jb250cmFjdHMuY3VzdG9tX2NyZWF0ZS5jb250cmFjdC5DdXN0b21DcmVhdGUuX19hbGdvcHlfZW50cnlwb2ludF93aXRoX2luaXQoKSAtPiB1aW50NjQ6Cm1haW46CiAgICBpbnRjYmxvY2sgMCAxCiAgICBieXRlY2Jsb2NrICJhZ2UiCiAgICAvLyBzbWFydF9jb250cmFjdHMvY3VzdG9tX2NyZWF0ZS9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBDdXN0b21DcmVhdGUoQVJDNENvbnRyYWN0KToKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBtYWluX2FmdGVyX2lmX2Vsc2VANwogICAgcHVzaGJ5dGVzcyAweDQ4MzMzMWVlIDB4NTYyN2IzY2QgLy8gbWV0aG9kICJjdXN0b21fY3JlYXRlKHVpbnQ2NCl2b2lkIiwgbWV0aG9kICJnZXRfYWdlKCl1aW50NjQiCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBtYWluX2N1c3RvbV9jcmVhdGVfcm91dGVANSBtYWluX2dldF9hZ2Vfcm91dGVANgoKbWFpbl9hZnRlcl9pZl9lbHNlQDc6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY3VzdG9tX2NyZWF0ZS9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBDdXN0b21DcmVhdGUoQVJDNENvbnRyYWN0KToKICAgIGludGNfMCAvLyAwCiAgICByZXR1cm4KCm1haW5fZ2V0X2FnZV9yb3V0ZUA2OgogICAgLy8gc21hcnRfY29udHJhY3RzL2N1c3RvbV9jcmVhdGUvY29udHJhY3QucHk6MTQKICAgIC8vIEBhYmltZXRob2QoKQogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGdldF9hZ2UKICAgIGl0b2IKICAgIHB1c2hieXRlcyAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgaW50Y18xIC8vIDEKICAgIHJldHVybgoKbWFpbl9jdXN0b21fY3JlYXRlX3JvdXRlQDU6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY3VzdG9tX2NyZWF0ZS9jb250cmFjdC5weToxMAogICAgLy8gQGFiaW1ldGhvZChjcmVhdGU9InJlcXVpcmUiKQogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgICEKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gY3JlYXRpbmcKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jdXN0b21fY3JlYXRlL2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIEN1c3RvbUNyZWF0ZShBUkM0Q29udHJhY3QpOgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQogICAgYnRvaQogICAgLy8gc21hcnRfY29udHJhY3RzL2N1c3RvbV9jcmVhdGUvY29udHJhY3QucHk6MTAKICAgIC8vIEBhYmltZXRob2QoY3JlYXRlPSJyZXF1aXJlIikKICAgIGNhbGxzdWIgY3VzdG9tX2NyZWF0ZQogICAgaW50Y18xIC8vIDEKICAgIHJldHVybgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5jdXN0b21fY3JlYXRlLmNvbnRyYWN0LkN1c3RvbUNyZWF0ZS5jdXN0b21fY3JlYXRlKGFnZTogdWludDY0KSAtPiB2b2lkOgpjdXN0b21fY3JlYXRlOgogICAgLy8gc21hcnRfY29udHJhY3RzL2N1c3RvbV9jcmVhdGUvY29udHJhY3QucHk6MTAtMTEKICAgIC8vIEBhYmltZXRob2QoY3JlYXRlPSJyZXF1aXJlIikKICAgIC8vIGRlZiBjdXN0b21fY3JlYXRlKHNlbGYsIGFnZTogVUludDY0KSAtPiBOb25lOgogICAgcHJvdG8gMSAwCiAgICAvLyBzbWFydF9jb250cmFjdHMvY3VzdG9tX2NyZWF0ZS9jb250cmFjdC5weToxMgogICAgLy8gc2VsZi5hZ2UudmFsdWUgPSBhZ2UKICAgIGJ5dGVjXzAgLy8gImFnZSIKICAgIGZyYW1lX2RpZyAtMQogICAgYXBwX2dsb2JhbF9wdXQKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5jdXN0b21fY3JlYXRlLmNvbnRyYWN0LkN1c3RvbUNyZWF0ZS5nZXRfYWdlKCkgLT4gdWludDY0OgpnZXRfYWdlOgogICAgLy8gc21hcnRfY29udHJhY3RzL2N1c3RvbV9jcmVhdGUvY29udHJhY3QucHk6MTYKICAgIC8vIHJldHVybiBzZWxmLmFnZS52YWx1ZQogICAgaW50Y18wIC8vIDAKICAgIGJ5dGVjXzAgLy8gImFnZSIKICAgIGFwcF9nbG9iYWxfZ2V0X2V4CiAgICBhc3NlcnQgLy8gY2hlY2sgc2VsZi5hZ2UgZXhpc3RzCiAgICByZXRzdWIK", "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuY2xlYXJfc3RhdGVfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4K"}, "sourceInfo": {"approval": {"pcOffsetMethod": "none", "sourceInfo": [{"pc": [42, 64], "errorMessage": "OnCompletion is not NoOp"}, {"pc": [68], "errorMessage": "can only call when creating"}, {"pc": [45], "errorMessage": "can only call when not creating"}, {"pc": [89], "errorMessage": "check self.age exists"}]}, "clear": {"pcOffsetMethod": "none", "sourceInfo": []}}, "templateVariables": {}}"""
APP_SPEC = algokit_utils.Arc56Contract.from_json(_APP_SPEC_JSON)

def _parse_abi_args(args: object | None = None) -> list[object] | None:
    """Helper to parse ABI args into the format expected by underlying client"""
    if args is None:
        return None

    def convert_dataclass(value: object) -> object:
        if dataclasses.is_dataclass(value):
            return tuple(convert_dataclass(getattr(value, field.name)) for field in dataclasses.fields(value))
        elif isinstance(value, (list, tuple)):
            return type(value)(convert_dataclass(item) for item in value)
        return value

    match args:
        case tuple():
            method_args = list(args)
        case _ if dataclasses.is_dataclass(args):
            method_args = [getattr(args, field.name) for field in dataclasses.fields(args)]
        case _:
            raise ValueError("Invalid 'args' type. Expected 'tuple' or 'TypedDict' for respective typed arguments.")

    return [
        convert_dataclass(arg) if not isinstance(arg, algokit_utils.AppMethodCallTransactionArgument) else arg
        for arg in method_args
    ] if method_args else None

def _init_dataclass(cls: type, data: dict) -> object:
    """
    Recursively instantiate a dataclass of type `cls` from `data`.

    For each field on the dataclass, if the field type is also a dataclass
    and the corresponding data is a dict, instantiate that field recursively.
    """
    field_values = {}
    for field in dataclasses.fields(cls):
        field_value = data.get(field.name)
        # Check if the field expects another dataclass and the value is a dict.
        if dataclasses.is_dataclass(field.type) and isinstance(field_value, dict):
            field_values[field.name] = _init_dataclass(typing.cast(type, field.type), field_value)
        else:
            field_values[field.name] = field_value
    return cls(**field_values)

@dataclasses.dataclass(frozen=True, kw_only=True)
class CustomCreateArgs:
    """Dataclass for custom_create arguments"""
    age: int

    @property
    def abi_method_signature(self) -> str:
        return "custom_create(uint64)void"


class CustomCreateParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def get_age(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_age()uint64",
        }))

    def custom_create(
        self,
        args: tuple[int] | CustomCreateArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "custom_create(uint64)void",
            "args": method_args,
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> algokit_utils.AppCallParams:
        return self.app_client.params.bare.clear_state(
            params,
            
        )


class CustomCreateCreateTransactionParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def get_age(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_age()uint64",
        }))

    def custom_create(
        self,
        args: tuple[int] | CustomCreateArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "custom_create(uint64)void",
            "args": method_args,
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> Transaction:
        return self.app_client.create_transaction.bare.clear_state(
            params,
            
        )


class CustomCreateSend:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def get_age(
        self,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[int]:
    
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_age()uint64",
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[int], parsed_response)

    def custom_create(
        self,
        args: tuple[int] | CustomCreateArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[None]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "custom_create(uint64)void",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[None], parsed_response)

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[algokit_utils.ABIReturn]:
        return self.app_client.send.bare.clear_state(
            params,
            send_params=send_params,
        )


class GlobalStateValue(typing.TypedDict):
    """Shape of global_state state key values"""
    age: int

class CustomCreateState:
    """Methods to access state for the current CustomCreate app"""

    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    @property
    def global_state(
        self
    ) -> "_GlobalState":
            """Methods to access global_state for the current app"""
            return _GlobalState(self.app_client)

class _GlobalState:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client
        
        # Pre-generated mapping of value types to their struct classes
        self._struct_classes: dict[str, typing.Type[typing.Any]] = {}

    def get_all(self) -> GlobalStateValue:
        """Get all current keyed values from global_state state"""
        result = self.app_client.state.global_state.get_all()
        if not result:
            return typing.cast(GlobalStateValue, {})

        converted = {}
        for key, value in result.items():
            key_info = self.app_client.app_spec.state.keys.global_state.get(key)
            struct_class = self._struct_classes.get(key_info.value_type) if key_info else None
            converted[key] = (
                _init_dataclass(struct_class, value) if struct_class and isinstance(value, dict)
                else value
            )
        return typing.cast(GlobalStateValue, converted)

    @property
    def age(self) -> int:
        """Get the current value of the age key in global_state state"""
        value = self.app_client.state.global_state.get_value("age")
        if isinstance(value, dict) and "AVMUint64" in self._struct_classes:
            return _init_dataclass(self._struct_classes["AVMUint64"], value)  # type: ignore
        return typing.cast(int, value)

class CustomCreateClient:
    """Client for interacting with CustomCreate smart contract"""

    @typing.overload
    def __init__(self, app_client: algokit_utils.AppClient) -> None: ...
    
    @typing.overload
    def __init__(
        self,
        *,
        algorand: _AlgoKitAlgorandClient,
        app_id: int,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> None: ...

    def __init__(
        self,
        app_client: algokit_utils.AppClient | None = None,
        *,
        algorand: _AlgoKitAlgorandClient | None = None,
        app_id: int | None = None,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> None:
        if app_client:
            self.app_client = app_client
        elif algorand and app_id:
            self.app_client = algokit_utils.AppClient(
                algokit_utils.AppClientParams(
                    algorand=algorand,
                    app_spec=APP_SPEC,
                    app_id=app_id,
                    app_name=app_name,
                    default_sender=default_sender,
                    default_signer=default_signer,
                    approval_source_map=approval_source_map,
                    clear_source_map=clear_source_map,
                )
            )
        else:
            raise ValueError("Either app_client or algorand and app_id must be provided")
    
        self.params = CustomCreateParams(self.app_client)
        self.create_transaction = CustomCreateCreateTransactionParams(self.app_client)
        self.send = CustomCreateSend(self.app_client)
        self.state = CustomCreateState(self.app_client)

    @staticmethod
    def from_creator_and_name(
        creator_address: str,
        app_name: str,
        algorand: _AlgoKitAlgorandClient,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
        ignore_cache: bool | None = None,
        app_lookup_cache: algokit_utils.ApplicationLookup | None = None,
    ) -> "CustomCreateClient":
        return CustomCreateClient(
            algokit_utils.AppClient.from_creator_and_name(
                creator_address=creator_address,
                app_name=app_name,
                app_spec=APP_SPEC,
                algorand=algorand,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
                ignore_cache=ignore_cache,
                app_lookup_cache=app_lookup_cache,
            )
        )
    
    @staticmethod
    def from_network(
        algorand: _AlgoKitAlgorandClient,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> "CustomCreateClient":
        return CustomCreateClient(
            algokit_utils.AppClient.from_network(
                app_spec=APP_SPEC,
                algorand=algorand,
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    @property
    def app_id(self) -> int:
        return self.app_client.app_id
    
    @property
    def app_address(self) -> str:
        return self.app_client.app_address
    
    @property
    def app_name(self) -> str:
        return self.app_client.app_name
    
    @property
    def app_spec(self) -> algokit_utils.Arc56Contract:
        return self.app_client.app_spec
    
    @property
    def algorand(self) -> _AlgoKitAlgorandClient:
        return self.app_client.algorand

    def clone(
        self,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> "CustomCreateClient":
        return CustomCreateClient(
            self.app_client.clone(
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    def new_group(self) -> "CustomCreateComposer":
        return CustomCreateComposer(self)

    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["get_age()uint64"],
        return_value: algokit_utils.ABIReturn | None
    ) -> int | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["custom_create(uint64)void"],
        return_value: algokit_utils.ABIReturn | None
    ) -> None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: str,
        return_value: algokit_utils.ABIReturn | None
    ) -> algokit_utils.ABIValue | algokit_utils.ABIStruct | None: ...

    def decode_return_value(
        self,
        method: str,
        return_value: algokit_utils.ABIReturn | None
    ) -> algokit_utils.ABIValue | algokit_utils.ABIStruct | None | int:
        """Decode ABI return value for the given method."""
        if return_value is None:
            return None
    
        arc56_method = self.app_spec.get_arc56_method(method)
        decoded = return_value.get_arc56_value(arc56_method, self.app_spec.structs)
    
        # If method returns a struct, convert the dict to appropriate dataclass
        if (arc56_method and
            arc56_method.returns and
            arc56_method.returns.struct and
            isinstance(decoded, dict)):
            struct_class = globals().get(arc56_method.returns.struct)
            if struct_class:
                return struct_class(**typing.cast(dict, decoded))
        return decoded


@dataclasses.dataclass(frozen=True)
class CustomCreateMethodCallCreateParams(
    algokit_utils.AppClientCreateSchema, algokit_utils.BaseAppClientMethodCallParams[
        CustomCreateArgs,
        str | None,
    ]
):
    """Parameters for creating CustomCreate contract using ABI"""
    on_complete: typing.Literal[OnComplete.NoOpOC] | None = None
    method: str | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientMethodCallCreateParams:
        method_args = _parse_abi_args(self.args)
        return algokit_utils.AppClientMethodCallCreateParams(
            **{
                **self.__dict__,
                "method": self.method or getattr(self.args, "abi_method_signature", None),
                "args": method_args,
            }
        )

class CustomCreateFactory(algokit_utils.TypedAppFactoryProtocol[CustomCreateMethodCallCreateParams, None, None]):
    """Factory for deploying and managing CustomCreateClient smart contracts"""

    def __init__(
        self,
        algorand: _AlgoKitAlgorandClient,
        *,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        version: str | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
    ):
        self.app_factory = algokit_utils.AppFactory(
            params=algokit_utils.AppFactoryParams(
                algorand=algorand,
                app_spec=APP_SPEC,
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                version=version,
                compilation_params=compilation_params,
            )
        )
        self.params = CustomCreateFactoryParams(self.app_factory)
        self.create_transaction = CustomCreateFactoryCreateTransaction(self.app_factory)
        self.send = CustomCreateFactorySend(self.app_factory)

    @property
    def app_name(self) -> str:
        return self.app_factory.app_name
    
    @property
    def app_spec(self) -> algokit_utils.Arc56Contract:
        return self.app_factory.app_spec
    
    @property
    def algorand(self) -> _AlgoKitAlgorandClient:
        return self.app_factory.algorand

    def deploy(
        self,
        *,
        on_update: algokit_utils.OnUpdate | None = None,
        on_schema_break: algokit_utils.OnSchemaBreak | None = None,
        create_params: CustomCreateMethodCallCreateParams | None = None,
        update_params: None = None,
        delete_params: None = None,
        existing_deployments: algokit_utils.ApplicationLookup | None = None,
        ignore_cache: bool = False,
        app_name: str | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
    ) -> tuple[CustomCreateClient, algokit_utils.AppFactoryDeployResult]:
        """Deploy the application"""
        deploy_response = self.app_factory.deploy(
            on_update=on_update,
            on_schema_break=on_schema_break,
            create_params=create_params.to_algokit_utils_params() if create_params else None,
            update_params=update_params,
            delete_params=delete_params,
            existing_deployments=existing_deployments,
            ignore_cache=ignore_cache,
            app_name=app_name,
            compilation_params=compilation_params,
            send_params=send_params,
        )

        return CustomCreateClient(deploy_response[0]), deploy_response[1]

    def get_app_client_by_creator_and_name(
        self,
        creator_address: str,
        app_name: str,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        ignore_cache: bool | None = None,
        app_lookup_cache: algokit_utils.ApplicationLookup | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> CustomCreateClient:
        """Get an app client by creator address and name"""
        return CustomCreateClient(
            self.app_factory.get_app_client_by_creator_and_name(
                creator_address,
                app_name,
                default_sender,
                default_signer,
                ignore_cache,
                app_lookup_cache,
                approval_source_map,
                clear_source_map,
            )
        )

    def get_app_client_by_id(
        self,
        app_id: int,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> CustomCreateClient:
        """Get an app client by app ID"""
        return CustomCreateClient(
            self.app_factory.get_app_client_by_id(
                app_id,
                app_name,
                default_sender,
                default_signer,
                approval_source_map,
                clear_source_map,
            )
        )


class CustomCreateFactoryParams:
    """Parameters for creating transactions for CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = CustomCreateFactoryCreateParams(app_factory)
        self.update = CustomCreateFactoryUpdateParams(app_factory)
        self.delete = CustomCreateFactoryDeleteParams(app_factory)

class CustomCreateFactoryCreateParams:
    """Parameters for 'create' operations of CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateParams:
        """Creates an instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
            compilation_params=compilation_params)

    def get_age(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:
        """Creates a new instance using the get_age()uint64 ABI method"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "get_age()uint64",
                "args": None,
                }
            ),
            compilation_params=compilation_params
        )

    def custom_create(
        self,
        args: tuple[int] | CustomCreateArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:
        """Creates a new instance using the custom_create(uint64)void ABI method"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "custom_create(uint64)void",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

class CustomCreateFactoryUpdateParams:
    """Parameters for 'update' operations of CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        
    ) -> algokit_utils.AppUpdateParams:
        """Updates an instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.bare.deploy_update(
            algokit_utils.AppClientBareCallParams(**dataclasses.asdict(params)),
            )

class CustomCreateFactoryDeleteParams:
    """Parameters for 'delete' operations of CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        
    ) -> algokit_utils.AppDeleteParams:
        """Deletes an instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.bare.deploy_delete(
            algokit_utils.AppClientBareCallParams(**dataclasses.asdict(params)),
            )


class CustomCreateFactoryCreateTransaction:
    """Create transactions for CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = CustomCreateFactoryCreateTransactionCreate(app_factory)


class CustomCreateFactoryCreateTransactionCreate:
    """Create new instances of CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
    ) -> Transaction:
        """Creates a new instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.create_transaction.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
        )


class CustomCreateFactorySend:
    """Send calls to CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = CustomCreateFactorySendCreate(app_factory)


class CustomCreateFactorySendCreate:
    """Send create calls to CustomCreate contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
    ) -> tuple[CustomCreateClient, algokit_utils.SendAppCreateTransactionResult]:
        """Creates a new instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        result = self.app_factory.send.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
            send_params=send_params,
            compilation_params=compilation_params
        )
        return CustomCreateClient(result[0]), result[1]

    def custom_create(
        self,
        args: tuple[int] | CustomCreateArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> tuple[CustomCreateClient, algokit_utils.AppFactoryCreateMethodCallResult[None]]:
            """Creates and sends a transaction using the custom_create(uint64)void ABI method"""
            params = params or algokit_utils.CommonAppCallCreateParams()
            client, result = self.app_factory.send.create(
                algokit_utils.AppFactoryCreateMethodCallParams(
                    **{
                    **dataclasses.asdict(params),
                    "method": "custom_create(uint64)void",
                    "args": _parse_abi_args(args),
                    }
                ),
                send_params=send_params,
                compilation_params=compilation_params
            )
            return_value = None if result.abi_return is None else typing.cast(None, result.abi_return)
    
            return CustomCreateClient(client), algokit_utils.AppFactoryCreateMethodCallResult[None](
                **{
                    **result.__dict__,
                    "app_id": result.app_id,
                    "abi_return": return_value,
                    "transaction": result.transaction,
                    "confirmation": result.confirmation,
                    "group_id": result.group_id,
                    "tx_ids": result.tx_ids,
                    "transactions": result.transactions,
                    "confirmations": result.confirmations,
                    "app_address": result.app_address,
                }
            )


class CustomCreateComposer:
    """Composer for creating transaction groups for CustomCreate contract calls"""

    def __init__(self, client: "CustomCreateClient"):
        self.client = client
        self._composer = client.algorand.new_group()
        self._result_mappers: list[typing.Callable[[algokit_utils.ABIReturn | None], object] | None] = []

    def get_age(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "CustomCreateComposer":
        self._composer.add_app_call_method_call(
            self.client.params.get_age(
                
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "get_age()uint64", v
            )
        )
        return self

    def custom_create(
        self,
        args: tuple[int] | CustomCreateArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "CustomCreateComposer":
        self._composer.add_app_call_method_call(
            self.client.params.custom_create(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "custom_create(uint64)void", v
            )
        )
        return self

    def clear_state(
        self,
        *,
        args: list[bytes] | None = None,
        params: algokit_utils.CommonAppCallParams | None = None,
    ) -> "CustomCreateComposer":
        params=params or algokit_utils.CommonAppCallParams()
        self._composer.add_app_call(
            self.client.params.clear_state(
                algokit_utils.AppClientBareCallParams(
                    **{
                        **dataclasses.asdict(params),
                        "args": args
                    }
                )
            )
        )
        return self
    
    def add_transaction(
        self, txn: Transaction, signer: TransactionSigner | None = None
    ) -> "CustomCreateComposer":
        self._composer.add_transaction(txn, signer)
        return self
    
    def composer(self) -> algokit_utils.TransactionComposer:
        return self._composer
    
    def simulate(
        self,
        allow_more_logs: bool | None = None,
        allow_empty_signatures: bool | None = None,
        allow_unnamed_resources: bool | None = None,
        extra_opcode_budget: int | None = None,
        exec_trace_config: SimulateTraceConfig | None = None,
        simulation_round: int | None = None,
        skip_signatures: bool | None = None,
    ) -> algokit_utils.SendAtomicTransactionComposerResults:
        return self._composer.simulate(
            allow_more_logs=allow_more_logs,
            allow_empty_signatures=allow_empty_signatures,
            allow_unnamed_resources=allow_unnamed_resources,
            extra_opcode_budget=extra_opcode_budget,
            exec_trace_config=exec_trace_config,
            simulation_round=simulation_round,
            skip_signatures=skip_signatures,
        )
    
    def send(
        self,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAtomicTransactionComposerResults:
        return self._composer.send(send_params)
