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

_APP_SPEC_JSON = r"""{"arcs": [22, 28], "bareActions": {"call": [], "create": ["NoOp"]}, "methods": [{"actions": {"call": ["NoOp"], "create": []}, "args": [{"type": "uint64", "name": "account_balance"}], "name": "is_rich", "returns": {"type": "string"}, "events": [], "readonly": false, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [{"type": "uint64", "name": "number"}], "name": "is_even", "returns": {"type": "string"}, "events": [], "readonly": false, "recommendations": {}}], "name": "IfElseExample", "state": {"keys": {"box": {}, "global": {}, "local": {}}, "maps": {"box": {}, "global": {}, "local": {}}, "schema": {"global": {"bytes": 0, "ints": 0}, "local": {"bytes": 0, "ints": 0}}}, "structs": {}, "byteCode": {"approval": "CiYBBBUffHUxG0EAUoICBDfAEJAEZjLC1jYaAI4CACAAA4EAQzEZFEQxGEQ2GgEXiACcSRUWVwYCTFAoTFCwgQFDMRkURDEYRDYaAReIABtJFRZXBgJMUChMULCBAUMxGUD/vjEYFESBAUOKAQGL/4HoBw1BABiAFVRoaXMgYWNjb3VudCBpcyByaWNoIYmL/4FkDUEAHoAbVGhpcyBhY2NvdW50IGlzIGRvaW5nIHdlbGwuiYAXVGhpcyBhY2NvdW50IGlzIHBvb3IgOiiJigEBi/+BAhhAAAeABEV2ZW6JgANPZGSJ", "clear": "CoEBQw=="}, "compilerInfo": {"compiler": "puya", "compilerVersion": {"major": 4, "minor": 5, "patch": 3}}, "events": [], "networks": {}, "source": {"approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuYXBwcm92YWxfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIGJ5dGVjYmxvY2sgMHgxNTFmN2M3NQogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBJZkVsc2VFeGFtcGxlKEFSQzRDb250cmFjdCk6CiAgICB0eG4gTnVtQXBwQXJncwogICAgYnogbWFpbl9iYXJlX3JvdXRpbmdANwogICAgcHVzaGJ5dGVzcyAweDM3YzAxMDkwIDB4NjYzMmMyZDYgLy8gbWV0aG9kICJpc19yaWNoKHVpbnQ2NClzdHJpbmciLCBtZXRob2QgImlzX2V2ZW4odWludDY0KXN0cmluZyIKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDAKICAgIG1hdGNoIG1haW5faXNfcmljaF9yb3V0ZUAzIG1haW5faXNfZXZlbl9yb3V0ZUA0CgptYWluX2FmdGVyX2lmX2Vsc2VAMTE6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIElmRWxzZUV4YW1wbGUoQVJDNENvbnRyYWN0KToKICAgIHB1c2hpbnQgMCAvLyAwCiAgICByZXR1cm4KCm1haW5faXNfZXZlbl9yb3V0ZUA0OgogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weToxOS0yMAogICAgLy8gIyBleGFtcGxlOiBURVJOQVJZCiAgICAvLyBAYXJjNC5hYmltZXRob2QKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgbm90IE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBJZkVsc2VFeGFtcGxlKEFSQzRDb250cmFjdCk6CiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBidG9pCiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjE5LTIwCiAgICAvLyAjIGV4YW1wbGU6IFRFUk5BUlkKICAgIC8vIEBhcmM0LmFiaW1ldGhvZAogICAgY2FsbHN1YiBpc19ldmVuCiAgICBkdXAKICAgIGxlbgogICAgaXRvYgogICAgZXh0cmFjdCA2IDIKICAgIHN3YXAKICAgIGNvbmNhdAogICAgYnl0ZWNfMCAvLyAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgcHVzaGludCAxIC8vIDEKICAgIHJldHVybgoKbWFpbl9pc19yaWNoX3JvdXRlQDM6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjctOAogICAgLy8gIyBleGFtcGxlOiBJRl9FTFNFCiAgICAvLyBAYXJjNC5hYmltZXRob2QKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgbm90IE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBJZkVsc2VFeGFtcGxlKEFSQzRDb250cmFjdCk6CiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBidG9pCiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjctOAogICAgLy8gIyBleGFtcGxlOiBJRl9FTFNFCiAgICAvLyBAYXJjNC5hYmltZXRob2QKICAgIGNhbGxzdWIgaXNfcmljaAogICAgZHVwCiAgICBsZW4KICAgIGl0b2IKICAgIGV4dHJhY3QgNiAyCiAgICBzd2FwCiAgICBjb25jYXQKICAgIGJ5dGVjXzAgLy8gMHgxNTFmN2M3NQogICAgc3dhcAogICAgY29uY2F0CiAgICBsb2cKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4KCm1haW5fYmFyZV9yb3V0aW5nQDc6CiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIElmRWxzZUV4YW1wbGUoQVJDNENvbnRyYWN0KToKICAgIHR4biBPbkNvbXBsZXRpb24KICAgIGJueiBtYWluX2FmdGVyX2lmX2Vsc2VAMTEKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICAhCiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIGNyZWF0aW5nCiAgICBwdXNoaW50IDEgLy8gMQogICAgcmV0dXJuCgoKLy8gc21hcnRfY29udHJhY3RzLmNvbnRyb2xfZmxvdy5jb250cmFjdC5JZkVsc2VFeGFtcGxlLmlzX3JpY2goYWNjb3VudF9iYWxhbmNlOiB1aW50NjQpIC0+IGJ5dGVzOgppc19yaWNoOgogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weTo3LTkKICAgIC8vICMgZXhhbXBsZTogSUZfRUxTRQogICAgLy8gQGFyYzQuYWJpbWV0aG9kCiAgICAvLyBkZWYgaXNfcmljaChzZWxmLCBhY2NvdW50X2JhbGFuY2U6IFVJbnQ2NCkgLT4gU3RyaW5nOgogICAgcHJvdG8gMSAxCiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjEwCiAgICAvLyBpZiBhY2NvdW50X2JhbGFuY2UgPiAxMDAwOgogICAgZnJhbWVfZGlnIC0xCiAgICBwdXNoaW50IDEwMDAgLy8gMTAwMAogICAgPgogICAgYnogaXNfcmljaF9lbHNlX2JvZHlAMgogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weToxMQogICAgLy8gcmV0dXJuIFN0cmluZygiVGhpcyBhY2NvdW50IGlzIHJpY2ghIikKICAgIHB1c2hieXRlcyAiVGhpcyBhY2NvdW50IGlzIHJpY2ghIgogICAgcmV0c3ViCgppc19yaWNoX2Vsc2VfYm9keUAyOgogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weToxMgogICAgLy8gZWxpZiBhY2NvdW50X2JhbGFuY2UgPiAxMDA6CiAgICBmcmFtZV9kaWcgLTEKICAgIHB1c2hpbnQgMTAwIC8vIDEwMAogICAgPgogICAgYnogaXNfcmljaF9lbHNlX2JvZHlANAogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weToxMwogICAgLy8gcmV0dXJuIFN0cmluZygiVGhpcyBhY2NvdW50IGlzIGRvaW5nIHdlbGwuIikKICAgIHB1c2hieXRlcyAiVGhpcyBhY2NvdW50IGlzIGRvaW5nIHdlbGwuIgogICAgcmV0c3ViCgppc19yaWNoX2Vsc2VfYm9keUA0OgogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weToxNQogICAgLy8gcmV0dXJuIFN0cmluZygiVGhpcyBhY2NvdW50IGlzIHBvb3IgOigiKQogICAgcHVzaGJ5dGVzICJUaGlzIGFjY291bnQgaXMgcG9vciA6KCIKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5jb250cm9sX2Zsb3cuY29udHJhY3QuSWZFbHNlRXhhbXBsZS5pc19ldmVuKG51bWJlcjogdWludDY0KSAtPiBieXRlczoKaXNfZXZlbjoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9jb250cm9sX2Zsb3cvY29udHJhY3QucHk6MTktMjEKICAgIC8vICMgZXhhbXBsZTogVEVSTkFSWQogICAgLy8gQGFyYzQuYWJpbWV0aG9kCiAgICAvLyBkZWYgaXNfZXZlbihzZWxmLCBudW1iZXI6IFVJbnQ2NCkgLT4gU3RyaW5nOgogICAgcHJvdG8gMSAxCiAgICAvLyBzbWFydF9jb250cmFjdHMvY29udHJvbF9mbG93L2NvbnRyYWN0LnB5OjIyCiAgICAvLyByZXR1cm4gU3RyaW5nKCJFdmVuIikgaWYgbnVtYmVyICUgMiA9PSAwIGVsc2UgU3RyaW5nKCJPZGQiKQogICAgZnJhbWVfZGlnIC0xCiAgICBwdXNoaW50IDIgLy8gMgogICAgJQogICAgYm56IGlzX2V2ZW5fdGVybmFyeV9mYWxzZUAyCiAgICBwdXNoYnl0ZXMgIkV2ZW4iCiAgICByZXRzdWIKCmlzX2V2ZW5fdGVybmFyeV9mYWxzZUAyOgogICAgLy8gc21hcnRfY29udHJhY3RzL2NvbnRyb2xfZmxvdy9jb250cmFjdC5weToyMgogICAgLy8gcmV0dXJuIFN0cmluZygiRXZlbiIpIGlmIG51bWJlciAlIDIgPT0gMCBlbHNlIFN0cmluZygiT2RkIikKICAgIHB1c2hieXRlcyAiT2RkIgogICAgcmV0c3ViCg==", "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuY2xlYXJfc3RhdGVfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4K"}, "sourceInfo": {"approval": {"pcOffsetMethod": "none", "sourceInfo": [{"pc": [40, 69], "errorMessage": "OnCompletion is not NoOp"}, {"pc": [103], "errorMessage": "can only call when creating"}, {"pc": [43, 72], "errorMessage": "can only call when not creating"}]}, "clear": {"pcOffsetMethod": "none", "sourceInfo": []}}, "templateVariables": {}}"""
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
class IsRichArgs:
    """Dataclass for is_rich arguments"""
    account_balance: int

    @property
    def abi_method_signature(self) -> str:
        return "is_rich(uint64)string"

@dataclasses.dataclass(frozen=True, kw_only=True)
class IsEvenArgs:
    """Dataclass for is_even arguments"""
    number: int

    @property
    def abi_method_signature(self) -> str:
        return "is_even(uint64)string"


class IfElseExampleParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def is_rich(
        self,
        args: tuple[int] | IsRichArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "is_rich(uint64)string",
            "args": method_args,
        }))

    def is_even(
        self,
        args: tuple[int] | IsEvenArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "is_even(uint64)string",
            "args": method_args,
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> algokit_utils.AppCallParams:
        return self.app_client.params.bare.clear_state(
            params,
            
        )


class IfElseExampleCreateTransactionParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def is_rich(
        self,
        args: tuple[int] | IsRichArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "is_rich(uint64)string",
            "args": method_args,
        }))

    def is_even(
        self,
        args: tuple[int] | IsEvenArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "is_even(uint64)string",
            "args": method_args,
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> Transaction:
        return self.app_client.create_transaction.bare.clear_state(
            params,
            
        )


class IfElseExampleSend:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def is_rich(
        self,
        args: tuple[int] | IsRichArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[str]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "is_rich(uint64)string",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[str], parsed_response)

    def is_even(
        self,
        args: tuple[int] | IsEvenArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[str]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "is_even(uint64)string",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[str], parsed_response)

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[algokit_utils.ABIReturn]:
        return self.app_client.send.bare.clear_state(
            params,
            send_params=send_params,
        )


class IfElseExampleState:
    """Methods to access state for the current IfElseExample app"""

    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

class IfElseExampleClient:
    """Client for interacting with IfElseExample smart contract"""

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
    
        self.params = IfElseExampleParams(self.app_client)
        self.create_transaction = IfElseExampleCreateTransactionParams(self.app_client)
        self.send = IfElseExampleSend(self.app_client)
        self.state = IfElseExampleState(self.app_client)

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
    ) -> "IfElseExampleClient":
        return IfElseExampleClient(
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
    ) -> "IfElseExampleClient":
        return IfElseExampleClient(
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
    ) -> "IfElseExampleClient":
        return IfElseExampleClient(
            self.app_client.clone(
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    def new_group(self) -> "IfElseExampleComposer":
        return IfElseExampleComposer(self)

    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["is_rich(uint64)string"],
        return_value: algokit_utils.ABIReturn | None
    ) -> str | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["is_even(uint64)string"],
        return_value: algokit_utils.ABIReturn | None
    ) -> str | None: ...
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
    ) -> algokit_utils.ABIValue | algokit_utils.ABIStruct | None | str:
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
class IfElseExampleBareCallCreateParams(algokit_utils.AppClientBareCallCreateParams):
    """Parameters for creating IfElseExample contract with bare calls"""
    on_complete: typing.Literal[OnComplete.NoOpOC] | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientBareCallCreateParams:
        return algokit_utils.AppClientBareCallCreateParams(**self.__dict__)

class IfElseExampleFactory(algokit_utils.TypedAppFactoryProtocol[IfElseExampleBareCallCreateParams, None, None]):
    """Factory for deploying and managing IfElseExampleClient smart contracts"""

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
        self.params = IfElseExampleFactoryParams(self.app_factory)
        self.create_transaction = IfElseExampleFactoryCreateTransaction(self.app_factory)
        self.send = IfElseExampleFactorySend(self.app_factory)

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
        create_params: IfElseExampleBareCallCreateParams | None = None,
        update_params: None = None,
        delete_params: None = None,
        existing_deployments: algokit_utils.ApplicationLookup | None = None,
        ignore_cache: bool = False,
        app_name: str | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
    ) -> tuple[IfElseExampleClient, algokit_utils.AppFactoryDeployResult]:
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

        return IfElseExampleClient(deploy_response[0]), deploy_response[1]

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
    ) -> IfElseExampleClient:
        """Get an app client by creator address and name"""
        return IfElseExampleClient(
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
    ) -> IfElseExampleClient:
        """Get an app client by app ID"""
        return IfElseExampleClient(
            self.app_factory.get_app_client_by_id(
                app_id,
                app_name,
                default_sender,
                default_signer,
                approval_source_map,
                clear_source_map,
            )
        )


class IfElseExampleFactoryParams:
    """Parameters for creating transactions for IfElseExample contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = IfElseExampleFactoryCreateParams(app_factory)
        self.update = IfElseExampleFactoryUpdateParams(app_factory)
        self.delete = IfElseExampleFactoryDeleteParams(app_factory)

class IfElseExampleFactoryCreateParams:
    """Parameters for 'create' operations of IfElseExample contract"""

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

    def is_rich(
        self,
        args: tuple[int] | IsRichArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:
        """Creates a new instance using the is_rich(uint64)string ABI method"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "is_rich(uint64)string",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

    def is_even(
        self,
        args: tuple[int] | IsEvenArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:
        """Creates a new instance using the is_even(uint64)string ABI method"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "is_even(uint64)string",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

class IfElseExampleFactoryUpdateParams:
    """Parameters for 'update' operations of IfElseExample contract"""

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

class IfElseExampleFactoryDeleteParams:
    """Parameters for 'delete' operations of IfElseExample contract"""

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


class IfElseExampleFactoryCreateTransaction:
    """Create transactions for IfElseExample contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = IfElseExampleFactoryCreateTransactionCreate(app_factory)


class IfElseExampleFactoryCreateTransactionCreate:
    """Create new instances of IfElseExample contract"""

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


class IfElseExampleFactorySend:
    """Send calls to IfElseExample contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = IfElseExampleFactorySendCreate(app_factory)


class IfElseExampleFactorySendCreate:
    """Send create calls to IfElseExample contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
    ) -> tuple[IfElseExampleClient, algokit_utils.SendAppCreateTransactionResult]:
        """Creates a new instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        result = self.app_factory.send.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
            send_params=send_params,
            compilation_params=compilation_params
        )
        return IfElseExampleClient(result[0]), result[1]


class IfElseExampleComposer:
    """Composer for creating transaction groups for IfElseExample contract calls"""

    def __init__(self, client: "IfElseExampleClient"):
        self.client = client
        self._composer = client.algorand.new_group()
        self._result_mappers: list[typing.Callable[[algokit_utils.ABIReturn | None], object] | None] = []

    def is_rich(
        self,
        args: tuple[int] | IsRichArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "IfElseExampleComposer":
        self._composer.add_app_call_method_call(
            self.client.params.is_rich(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "is_rich(uint64)string", v
            )
        )
        return self

    def is_even(
        self,
        args: tuple[int] | IsEvenArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "IfElseExampleComposer":
        self._composer.add_app_call_method_call(
            self.client.params.is_even(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "is_even(uint64)string", v
            )
        )
        return self

    def clear_state(
        self,
        *,
        args: list[bytes] | None = None,
        params: algokit_utils.CommonAppCallParams | None = None,
    ) -> "IfElseExampleComposer":
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
    ) -> "IfElseExampleComposer":
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
