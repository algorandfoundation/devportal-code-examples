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

_APP_SPEC_JSON = r"""{"arcs": [22, 28], "bareActions": {"call": [], "create": ["NoOp"]}, "methods": [{"actions": {"call": ["NoOp"], "create": []}, "args": [], "name": "get_asset_balance", "returns": {"type": "uint64"}, "events": [], "readonly": false, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [{"type": "account", "name": "acct"}, {"type": "asset", "name": "asset"}], "name": "get_asset_balance_with_arg", "returns": {"type": "uint64"}, "events": [], "readonly": false, "recommendations": {}}], "name": "AccountAndAssetReference", "state": {"keys": {"box": {}, "global": {}, "local": {}}, "maps": {"box": {}, "global": {}, "local": {}}, "schema": {"global": {"bytes": 0, "ints": 0}, "local": {"bytes": 0, "ints": 0}}}, "structs": {}, "byteCode": {"approval": "CiACAAEmAQQVH3x1MRtBAEWCAgSmXnuWBDMTSVo2GgCOAgAfAAIiQzEZFEQxGEQ2GgEXwBw2GgIXwDCIAFcWKExQsCNDMRkURDEYRIgAEhYoTFCwI0MxGUD/yzEYFEQjQ4oAAYAgsw5eFWlqsaC8qv4fXqB+dn66jDoPvZncgGLXpt+WTmKBoQlwAEEABIsATIkiTImKAgGL/ov/cABBAASLAEyJIkyJ", "clear": "CoEBQw=="}, "compilerInfo": {"compiler": "puya", "compilerVersion": {"major": 4, "minor": 5, "patch": 3}}, "events": [], "networks": {}, "source": {"approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuYXBwcm92YWxfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIGludGNibG9jayAwIDEKICAgIGJ5dGVjYmxvY2sgMHgxNTFmN2M3NQogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjUKICAgIC8vIGNsYXNzIEFjY291bnRBbmRBc3NldFJlZmVyZW5jZShBUkM0Q29udHJhY3QpOgogICAgdHhuIE51bUFwcEFyZ3MKICAgIGJ6IG1haW5fYmFyZV9yb3V0aW5nQDcKICAgIHB1c2hieXRlc3MgMHhhNjVlN2I5NiAweDMzMTM0OTVhIC8vIG1ldGhvZCAiZ2V0X2Fzc2V0X2JhbGFuY2UoKXVpbnQ2NCIsIG1ldGhvZCAiZ2V0X2Fzc2V0X2JhbGFuY2Vfd2l0aF9hcmcoYWNjb3VudCxhc3NldCl1aW50NjQiCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBtYWluX2dldF9hc3NldF9iYWxhbmNlX3JvdXRlQDMgbWFpbl9nZXRfYXNzZXRfYmFsYW5jZV93aXRoX2FyZ19yb3V0ZUA0CgptYWluX2FmdGVyX2lmX2Vsc2VAMTE6CiAgICAvLyBzbWFydF9jb250cmFjdHMvcmVmZXJlbmNlX2FjY291bnRfYXNzZXQvY29udHJhY3QucHk6NQogICAgLy8gY2xhc3MgQWNjb3VudEFuZEFzc2V0UmVmZXJlbmNlKEFSQzRDb250cmFjdCk6CiAgICBpbnRjXzAgLy8gMAogICAgcmV0dXJuCgptYWluX2dldF9hc3NldF9iYWxhbmNlX3dpdGhfYXJnX3JvdXRlQDQ6CiAgICAvLyBzbWFydF9jb250cmFjdHMvcmVmZXJlbmNlX2FjY291bnRfYXNzZXQvY29udHJhY3QucHk6MTkKICAgIC8vIEBhYmltZXRob2QKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgbm90IE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjUKICAgIC8vIGNsYXNzIEFjY291bnRBbmRBc3NldFJlZmVyZW5jZShBUkM0Q29udHJhY3QpOgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQogICAgYnRvaQogICAgdHhuYXMgQWNjb3VudHMKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDIKICAgIGJ0b2kKICAgIHR4bmFzIEFzc2V0cwogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjE5CiAgICAvLyBAYWJpbWV0aG9kCiAgICBjYWxsc3ViIGdldF9hc3NldF9iYWxhbmNlX3dpdGhfYXJnCiAgICBpdG9iCiAgICBieXRlY18wIC8vIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnRjXzEgLy8gMQogICAgcmV0dXJuCgptYWluX2dldF9hc3NldF9iYWxhbmNlX3JvdXRlQDM6CiAgICAvLyBzbWFydF9jb250cmFjdHMvcmVmZXJlbmNlX2FjY291bnRfYXNzZXQvY29udHJhY3QucHk6NwogICAgLy8gQGFiaW1ldGhvZAogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGdldF9hc3NldF9iYWxhbmNlCiAgICBpdG9iCiAgICBieXRlY18wIC8vIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnRjXzEgLy8gMQogICAgcmV0dXJuCgptYWluX2JhcmVfcm91dGluZ0A3OgogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjUKICAgIC8vIGNsYXNzIEFjY291bnRBbmRBc3NldFJlZmVyZW5jZShBUkM0Q29udHJhY3QpOgogICAgdHhuIE9uQ29tcGxldGlvbgogICAgYm56IG1haW5fYWZ0ZXJfaWZfZWxzZUAxMQogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgICEKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gY3JlYXRpbmcKICAgIGludGNfMSAvLyAxCiAgICByZXR1cm4KCgovLyBzbWFydF9jb250cmFjdHMucmVmZXJlbmNlX2FjY291bnRfYXNzZXQuY29udHJhY3QuQWNjb3VudEFuZEFzc2V0UmVmZXJlbmNlLmdldF9hc3NldF9iYWxhbmNlKCkgLT4gdWludDY0OgpnZXRfYXNzZXRfYmFsYW5jZToKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9yZWZlcmVuY2VfYWNjb3VudF9hc3NldC9jb250cmFjdC5weTo3LTgKICAgIC8vIEBhYmltZXRob2QKICAgIC8vIGRlZiBnZXRfYXNzZXRfYmFsYW5jZShzZWxmKSAtPiBVSW50NjQ6CiAgICBwcm90byAwIDEKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9yZWZlcmVuY2VfYWNjb3VudF9hc3NldC9jb250cmFjdC5weTo5LTExCiAgICAvLyBhY2N0ID0gQWNjb3VudCgKICAgIC8vICAgICAiV01IRjRGTEpOS1kyQlBGSzdZUFY1SUQ2T1o3TFZEQjJCNjZaVFhFQU1MTDJOWDRXSlpSSkZWWDY2TSIKICAgIC8vICkgICMgUmVwbGFjZSB3aXRoIHlvdXIgYWNjb3VudCBhZGRyZXNzCiAgICBwdXNoYnl0ZXMgYmFzZTMyKFdNSEY0RkxKTktZMkJQRks3WVBWNUlENk9aN0xWREIyQjY2WlRYRUFNTEwyTlg0V0paUkEpIC8vIGFkZHIgV01IRjRGTEpOS1kyQlBGSzdZUFY1SUQ2T1o3TFZEQjJCNjZaVFhFQU1MTDJOWDRXSlpSSkZWWDY2TQogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjEyCiAgICAvLyBhc3NldCA9IEFzc2V0KDExODUpICAjIFJlcGxhY2Ugd2l0aCB5b3VyIGFzc2V0IGlkCiAgICBwdXNoaW50IDExODUgLy8gMTE4NQogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjEzCiAgICAvLyBiYWxhbmNlLCBoYXNfdmFsdWUgPSBvcC5Bc3NldEhvbGRpbmdHZXQuYXNzZXRfYmFsYW5jZShhY2N0LCBhc3NldCkKICAgIGFzc2V0X2hvbGRpbmdfZ2V0IEFzc2V0QmFsYW5jZQogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjE1CiAgICAvLyBpZiBoYXNfdmFsdWU6CiAgICBieiBnZXRfYXNzZXRfYmFsYW5jZV9hZnRlcl9pZl9lbHNlQDIKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9yZWZlcmVuY2VfYWNjb3VudF9hc3NldC9jb250cmFjdC5weToxNgogICAgLy8gcmV0dXJuIGJhbGFuY2UKICAgIGZyYW1lX2RpZyAwCiAgICBzd2FwCiAgICByZXRzdWIKCmdldF9hc3NldF9iYWxhbmNlX2FmdGVyX2lmX2Vsc2VAMjoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9yZWZlcmVuY2VfYWNjb3VudF9hc3NldC9jb250cmFjdC5weToxNwogICAgLy8gcmV0dXJuIFVJbnQ2NCgwKQogICAgaW50Y18wIC8vIDAKICAgIHN3YXAKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5yZWZlcmVuY2VfYWNjb3VudF9hc3NldC5jb250cmFjdC5BY2NvdW50QW5kQXNzZXRSZWZlcmVuY2UuZ2V0X2Fzc2V0X2JhbGFuY2Vfd2l0aF9hcmcoYWNjdDogYnl0ZXMsIGFzc2V0OiB1aW50NjQpIC0+IHVpbnQ2NDoKZ2V0X2Fzc2V0X2JhbGFuY2Vfd2l0aF9hcmc6CiAgICAvLyBzbWFydF9jb250cmFjdHMvcmVmZXJlbmNlX2FjY291bnRfYXNzZXQvY29udHJhY3QucHk6MTktMjAKICAgIC8vIEBhYmltZXRob2QKICAgIC8vIGRlZiBnZXRfYXNzZXRfYmFsYW5jZV93aXRoX2FyZyhzZWxmLCBhY2N0OiBBY2NvdW50LCBhc3NldDogQXNzZXQpIC0+IFVJbnQ2NDoKICAgIHByb3RvIDIgMQogICAgLy8gc21hcnRfY29udHJhY3RzL3JlZmVyZW5jZV9hY2NvdW50X2Fzc2V0L2NvbnRyYWN0LnB5OjIxCiAgICAvLyBiYWxhbmNlLCBoYXNfdmFsdWUgPSBvcC5Bc3NldEhvbGRpbmdHZXQuYXNzZXRfYmFsYW5jZShhY2N0LCBhc3NldCkKICAgIGZyYW1lX2RpZyAtMgogICAgZnJhbWVfZGlnIC0xCiAgICBhc3NldF9ob2xkaW5nX2dldCBBc3NldEJhbGFuY2UKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9yZWZlcmVuY2VfYWNjb3VudF9hc3NldC9jb250cmFjdC5weToyMwogICAgLy8gaWYgaGFzX3ZhbHVlOgogICAgYnogZ2V0X2Fzc2V0X2JhbGFuY2Vfd2l0aF9hcmdfYWZ0ZXJfaWZfZWxzZUAyCiAgICAvLyBzbWFydF9jb250cmFjdHMvcmVmZXJlbmNlX2FjY291bnRfYXNzZXQvY29udHJhY3QucHk6MjQKICAgIC8vIHJldHVybiBiYWxhbmNlCiAgICBmcmFtZV9kaWcgMAogICAgc3dhcAogICAgcmV0c3ViCgpnZXRfYXNzZXRfYmFsYW5jZV93aXRoX2FyZ19hZnRlcl9pZl9lbHNlQDI6CiAgICAvLyBzbWFydF9jb250cmFjdHMvcmVmZXJlbmNlX2FjY291bnRfYXNzZXQvY29udHJhY3QucHk6MjUKICAgIC8vIHJldHVybiBVSW50NjQoMCkKICAgIGludGNfMCAvLyAwCiAgICBzd2FwCiAgICByZXRzdWIK", "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuY2xlYXJfc3RhdGVfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4K"}, "sourceInfo": {"approval": {"pcOffsetMethod": "none", "sourceInfo": [{"pc": [43, 72], "errorMessage": "OnCompletion is not NoOp"}, {"pc": [94], "errorMessage": "can only call when creating"}, {"pc": [46, 75], "errorMessage": "can only call when not creating"}]}, "clear": {"pcOffsetMethod": "none", "sourceInfo": []}}, "templateVariables": {}}"""
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
class GetAssetBalanceWithArgArgs:
    """Dataclass for get_asset_balance_with_arg arguments"""
    acct: str | bytes
    asset: int

    @property
    def abi_method_signature(self) -> str:
        return "get_asset_balance_with_arg(account,asset)uint64"


class AccountAndAssetReferenceParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def get_asset_balance(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_asset_balance()uint64",
        }))

    def get_asset_balance_with_arg(
        self,
        args: tuple[str | bytes, int] | GetAssetBalanceWithArgArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_asset_balance_with_arg(account,asset)uint64",
            "args": method_args,
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> algokit_utils.AppCallParams:
        return self.app_client.params.bare.clear_state(
            params,
            
        )


class AccountAndAssetReferenceCreateTransactionParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def get_asset_balance(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_asset_balance()uint64",
        }))

    def get_asset_balance_with_arg(
        self,
        args: tuple[str | bytes, int] | GetAssetBalanceWithArgArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_asset_balance_with_arg(account,asset)uint64",
            "args": method_args,
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> Transaction:
        return self.app_client.create_transaction.bare.clear_state(
            params,
            
        )


class AccountAndAssetReferenceSend:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def get_asset_balance(
        self,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[int]:
    
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_asset_balance()uint64",
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[int], parsed_response)

    def get_asset_balance_with_arg(
        self,
        args: tuple[str | bytes, int] | GetAssetBalanceWithArgArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[int]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_asset_balance_with_arg(account,asset)uint64",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[int], parsed_response)

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[algokit_utils.ABIReturn]:
        return self.app_client.send.bare.clear_state(
            params,
            send_params=send_params,
        )


class AccountAndAssetReferenceState:
    """Methods to access state for the current AccountAndAssetReference app"""

    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

class AccountAndAssetReferenceClient:
    """Client for interacting with AccountAndAssetReference smart contract"""

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
    
        self.params = AccountAndAssetReferenceParams(self.app_client)
        self.create_transaction = AccountAndAssetReferenceCreateTransactionParams(self.app_client)
        self.send = AccountAndAssetReferenceSend(self.app_client)
        self.state = AccountAndAssetReferenceState(self.app_client)

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
    ) -> "AccountAndAssetReferenceClient":
        return AccountAndAssetReferenceClient(
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
    ) -> "AccountAndAssetReferenceClient":
        return AccountAndAssetReferenceClient(
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
    ) -> "AccountAndAssetReferenceClient":
        return AccountAndAssetReferenceClient(
            self.app_client.clone(
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    def new_group(self) -> "AccountAndAssetReferenceComposer":
        return AccountAndAssetReferenceComposer(self)

    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["get_asset_balance()uint64"],
        return_value: algokit_utils.ABIReturn | None
    ) -> int | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["get_asset_balance_with_arg(account,asset)uint64"],
        return_value: algokit_utils.ABIReturn | None
    ) -> int | None: ...
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
class AccountAndAssetReferenceBareCallCreateParams(algokit_utils.AppClientBareCallCreateParams):
    """Parameters for creating AccountAndAssetReference contract with bare calls"""
    on_complete: typing.Literal[OnComplete.NoOpOC] | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientBareCallCreateParams:
        return algokit_utils.AppClientBareCallCreateParams(**self.__dict__)

class AccountAndAssetReferenceFactory(algokit_utils.TypedAppFactoryProtocol[AccountAndAssetReferenceBareCallCreateParams, None, None]):
    """Factory for deploying and managing AccountAndAssetReferenceClient smart contracts"""

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
        self.params = AccountAndAssetReferenceFactoryParams(self.app_factory)
        self.create_transaction = AccountAndAssetReferenceFactoryCreateTransaction(self.app_factory)
        self.send = AccountAndAssetReferenceFactorySend(self.app_factory)

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
        create_params: AccountAndAssetReferenceBareCallCreateParams | None = None,
        update_params: None = None,
        delete_params: None = None,
        existing_deployments: algokit_utils.ApplicationLookup | None = None,
        ignore_cache: bool = False,
        app_name: str | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
    ) -> tuple[AccountAndAssetReferenceClient, algokit_utils.AppFactoryDeployResult]:
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

        return AccountAndAssetReferenceClient(deploy_response[0]), deploy_response[1]

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
    ) -> AccountAndAssetReferenceClient:
        """Get an app client by creator address and name"""
        return AccountAndAssetReferenceClient(
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
    ) -> AccountAndAssetReferenceClient:
        """Get an app client by app ID"""
        return AccountAndAssetReferenceClient(
            self.app_factory.get_app_client_by_id(
                app_id,
                app_name,
                default_sender,
                default_signer,
                approval_source_map,
                clear_source_map,
            )
        )


class AccountAndAssetReferenceFactoryParams:
    """Parameters for creating transactions for AccountAndAssetReference contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = AccountAndAssetReferenceFactoryCreateParams(app_factory)
        self.update = AccountAndAssetReferenceFactoryUpdateParams(app_factory)
        self.delete = AccountAndAssetReferenceFactoryDeleteParams(app_factory)

class AccountAndAssetReferenceFactoryCreateParams:
    """Parameters for 'create' operations of AccountAndAssetReference contract"""

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

    def get_asset_balance(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:
        """Creates a new instance using the get_asset_balance()uint64 ABI method"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "get_asset_balance()uint64",
                "args": None,
                }
            ),
            compilation_params=compilation_params
        )

    def get_asset_balance_with_arg(
        self,
        args: tuple[str | bytes, int] | GetAssetBalanceWithArgArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:
        """Creates a new instance using the get_asset_balance_with_arg(account,asset)uint64 ABI method"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "get_asset_balance_with_arg(account,asset)uint64",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

class AccountAndAssetReferenceFactoryUpdateParams:
    """Parameters for 'update' operations of AccountAndAssetReference contract"""

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

class AccountAndAssetReferenceFactoryDeleteParams:
    """Parameters for 'delete' operations of AccountAndAssetReference contract"""

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


class AccountAndAssetReferenceFactoryCreateTransaction:
    """Create transactions for AccountAndAssetReference contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = AccountAndAssetReferenceFactoryCreateTransactionCreate(app_factory)


class AccountAndAssetReferenceFactoryCreateTransactionCreate:
    """Create new instances of AccountAndAssetReference contract"""

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


class AccountAndAssetReferenceFactorySend:
    """Send calls to AccountAndAssetReference contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = AccountAndAssetReferenceFactorySendCreate(app_factory)


class AccountAndAssetReferenceFactorySendCreate:
    """Send create calls to AccountAndAssetReference contract"""

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
    ) -> tuple[AccountAndAssetReferenceClient, algokit_utils.SendAppCreateTransactionResult]:
        """Creates a new instance using a bare call"""
        params = params or algokit_utils.CommonAppCallCreateParams()
        result = self.app_factory.send.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
            send_params=send_params,
            compilation_params=compilation_params
        )
        return AccountAndAssetReferenceClient(result[0]), result[1]


class AccountAndAssetReferenceComposer:
    """Composer for creating transaction groups for AccountAndAssetReference contract calls"""

    def __init__(self, client: "AccountAndAssetReferenceClient"):
        self.client = client
        self._composer = client.algorand.new_group()
        self._result_mappers: list[typing.Callable[[algokit_utils.ABIReturn | None], object] | None] = []

    def get_asset_balance(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "AccountAndAssetReferenceComposer":
        self._composer.add_app_call_method_call(
            self.client.params.get_asset_balance(
                
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "get_asset_balance()uint64", v
            )
        )
        return self

    def get_asset_balance_with_arg(
        self,
        args: tuple[str | bytes, int] | GetAssetBalanceWithArgArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "AccountAndAssetReferenceComposer":
        self._composer.add_app_call_method_call(
            self.client.params.get_asset_balance_with_arg(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "get_asset_balance_with_arg(account,asset)uint64", v
            )
        )
        return self

    def clear_state(
        self,
        *,
        args: list[bytes] | None = None,
        params: algokit_utils.CommonAppCallParams | None = None,
    ) -> "AccountAndAssetReferenceComposer":
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
    ) -> "AccountAndAssetReferenceComposer":
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
