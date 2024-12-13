import typing 
from algopy import ARC4Contract, Box, BoxMap, BoxRef, Bytes, Global, String, Txn, UInt64, arc4

StaticInts: typing.TypeAlias = arc4.StaticArray[arc4.UInt8, typing.Literal[4]]

class UserStruct(arc4.Struct):
    name: arc4.String
    id: arc4.UInt64
    asset: arc4.UInt64

# example: BOX_STORAGE
class BoxStorage(ARC4Contract):
    def __init__(self) -> None:
        ## Box storage
        self.box_int = Box(UInt64)
        self.box_dynamic_bytes = Box[arc4.DynamicBytes](arc4.DynamicBytes, key="b")
        self.box_string = Box(arc4.String, key=b"BOX_C")
        self.box_bytes = Box(Bytes)
        self.box_map = BoxMap(UInt64, String, key_prefix="") # Box map with uint as key and string as value
        self.box_ref = BoxRef() # Box reference
        self.box_map_struct = BoxMap(arc4.UInt64, UserStruct, key_prefix="users")
        
    ## Box
    ### Bool
    @arc4.abimethod
    def box_exist(self) -> bool:
        return bool(self.box_int)

    @arc4.abimethod
    def box_exist_example(self) -> tuple[bool, bool, bool]:
        return bool(self.box_dynamic_bytes), bool(self.box_string), bool(self.box_bytes)
    
    ### Property key
    @arc4.abimethod
    def key_box(self) -> Bytes:
        return self.box_int.key

    @arc4.abimethod
    def key_box_example(self) -> None:
        assert self.box_dynamic_bytes.key == b"b", "box dynamic bytes key ok"
        assert self.box_string.key == b"BOX_STRING", "box string key ok"
        assert self.box_bytes.key == b"BOX_BYTES", "box bytes key ok"

    ### Get
    @arc4.abimethod
    def get_box(self) -> UInt64:
        return self.box_int.value
    
    @arc4.abimethod
    def get_box_example(self) -> tuple[UInt64, Bytes, arc4.String]:
        return self.box_int.value, self.box_dynamic_bytes.value.native, self.box_string.value
    
    ### Set
    @arc4.abimethod
    def set_box(self, value_int: UInt64) -> None:
        self.box_int.value = value_int

    @arc4.abimethod
    def set_box_example(self, value_int: UInt64, value_dbytes: arc4.DynamicBytes, value_string: arc4.String) -> None:
        self.box_int.value = value_int
        self.box_dynamic_bytes.value = value_dbytes.copy()
        self.box_string.value = value_string
        self.box_bytes.value = value_dbytes.native

        byte_value = self.box_dynamic_bytes.value.copy()
        assert self.box_dynamic_bytes.value.length == byte_value.length, "direct reference should match copy"

        self.box_int.value += 3
    
    ### Maybe
    @arc4.abimethod
    def maybe_box(self) -> tuple[UInt64, bool]:
        box_int_value, box_int_exists = self.box_int.maybe()
        return box_int_value, box_int_exists

    @arc4.abimethod
    def maybe_box_example(self) -> None:
        del self.box_int.value
        assert self.box_int.get(default=UInt64(42)) == 42
        box_int_value, box_int_exists = self.box_int.maybe()
        assert not box_int_exists
        assert box_int_value == 0

    ### Property value
    @arc4.abimethod
    def value_box(self) -> None:
        assert self.box_int.value == UInt64(10)

    ### Property length - fails if box doesn't exist: unrecognised member of algopy.Box

    ### Delete box
    @arc4.abimethod
    def delete_boxes(self) -> None:
        del self.box_int.value
        del self.box_dynamic_bytes.value
        del self.box_string.value
        
        assert self.box_int.get(default=UInt64(42)) == 42
        assert self.box_dynamic_bytes.get(default=arc4.DynamicBytes(b"42")).native == b"42"
        assert self.box_string.get(default=arc4.String("42")) == "42"

    ### Slice box
    @arc4.abimethod
    def slice_box(self) -> None:
        box_0 = Box(Bytes, key=String("0"))
        box_0.value = Bytes(b"Testing testing 123")
        assert box_0.value[0:7] == b"Testing"

        self.box_string.value = arc4.String("Hello")
        assert self.box_string.value.bytes[2:10] == b"Hello"

    @arc4.abimethod
    def arc4_box(self) -> None:
        box_bytes = Box(StaticInts, key=Bytes(b"d"))
        box_bytes.value = StaticInts(arc4.UInt8(0), arc4.UInt8(1), arc4.UInt8(2), arc4.UInt8(3))

        assert box_bytes.value[0] == 0
        assert box_bytes.value[1] == 1
        assert box_bytes.value[2] == 2
        assert box_bytes.value[3] == 3

    ## Box Reference: Property - key


    ### Box Reference: create
    @arc4.abimethod
    def create_box_ref(self) -> None:
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        assert box_ref.create(size=32)
        assert box_ref, "has data"

    ### Box Reference: delete
    @arc4.abimethod
    def test_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # instance box ref
        self.box_ref.create(size=UInt64(32))
        assert self.box_ref, "has data"
        self.box_ref.delete()

    ### Box Reference: extract
    @arc4.abimethod
    def extract_box_ref(self) -> None:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)

        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)
        box_ref.replace(64, value_3)
        prefix = box_ref.extract(0, 32 * 2 + value_3.length)
        assert prefix == app_address + sender_bytes + value_3

    ### Box Reference: resize - not implemented
    @arc4.abimethod
    def key_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)
        box_ref.replace(64, value_3)
        prefix = box_ref.extract(0, 32 * 2 + value_3.length)
        assert prefix == app_address + sender_bytes + value_3

        # delete
        assert box_ref.delete()
        assert box_ref.key == b"blob"

    ### Box Reference: replace
    @arc4.abimethod
    def replace_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)

    ### Box Reference: splice
    @arc4.abimethod
    def splice_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)

    ### Box Reference: get
    @arc4.abimethod
    def get_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)
        box_ref.replace(64, value_3)
        prefix = box_ref.extract(0, 32 * 2 + value_3.length)
        assert prefix == app_address + sender_bytes + value_3

        # delete
        assert box_ref.delete()
        assert box_ref.key == b"blob"

        # query
        value, exists = box_ref.maybe()
        assert not exists
        assert value == b""
        assert box_ref.get(default=sender_bytes) == sender_bytes

    ### Box Reference: put
    @arc4.abimethod
    def put_box_ref(self) -> None:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)
        
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes

        assert box_ref.delete()
        assert box_ref.key == b"blob"

        box_ref.put(sender_bytes + app_address)
        assert box_ref, "Blob exists"
        assert box_ref.length == 64

    ### Box Reference: maybe
    @arc4.abimethod
    def maybe_box_ref(self) -> tuple[Bytes, bool]:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)

        value, exists = box_ref.maybe()
        if not exists:
            value = Bytes(b"")
        return value, exists

    ### Box Reference: Property - length 
    @arc4.abimethod
    def length_box_ref(self) -> UInt64:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)
        return box_ref.length

    @arc4.abimethod
    def length_box_ref_example(self) -> None:
        box_ref = BoxRef(key="blob")
        assert box_ref.create(size=32)
        assert box_ref.length == 64

        box_ref = BoxRef(key=b"blob")
        assert box_ref.create(size=32)
        assert box_ref.length == 64

        box_ref = BoxRef(key=Bytes(b"blob"))
        assert box_ref.create(size=32)
        assert box_ref.length == 64

        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)
        assert box_ref.length == 64
        
    ### Box Map: key prefix
    @arc4.abimethod
    def key_prefix_box_map(self) -> Bytes:
        return self.box_map.key_prefix

    @arc4.abimethod
    def key_prefix_box_map_example(self) -> None:
        assert self.box_map.key_prefix == b""

    ### Box Map: get item
    @arc4.abimethod
    def box_map_get_item(self, key: UInt64) -> String:
        return self.box_map[key]
    
    ### Box Map: set item
    @arc4.abimethod
    def box_map_set(self, key: UInt64, value: String) -> None:
        self.box_map[key] = value

    ### Box Map: del item
    @arc4.abimethod
    def box_map_del(self, key: UInt64) -> None:
        del self.box_map[key]

    ### Box Map: contains
    @arc4.abimethod
    def box_map_exists(self, key: UInt64) -> bool:
        return key in self.box_map
    
    ### Box Map: get
    @arc4.abimethod
    def box_map_get(self) -> String:
        key_1 = UInt64(1)
        return self.box_map.get(key_1, default=String("default"))

    @arc4.abimethod
    def box_map_get_example(self) -> bool:
        key_1 = UInt64(1)
        assert self.box_map.get(key_1, default=String("default")) == String("default")
        return True

    ### Box Map: maybe
    @arc4.abimethod
    def maybe_box_map(self) -> tuple[String, bool]:
        key_1 = UInt64(1)
        value, exists = self.box_map.maybe(key_1)
        if not exists:
            value = String('')
        return value, exists
    
    @arc4.abimethod
    def maybe_box_map_example(self) -> None:
        key_0 = UInt64(0)
        key_1 = UInt64(1)
        value, exists = self.box_map.maybe(key_1)
        assert not exists
        assert key_0 in self.box_map

    ### Box Map: length
    @arc4.abimethod
    def box_map_length(self) -> UInt64:
        # fails if doesnt exist
        key_0 = UInt64(0)
        if not self.box_map:
            return UInt64(0)
        return self.box_map.length(key_0)

    @arc4.abimethod
    def box_map_length_example(self) -> None:
        key_0 = UInt64(0)
        value = String("Hmmmmm")
        self.box_map[key_0] = value
        assert self.box_map[key_0].bytes.length == value.bytes.length
        assert self.box_map.length(key_0) == value.bytes.length

    @arc4.abimethod
    def box_map_struct_length(self) -> bool:
        key_0 = arc4.UInt64(0)
        key_1 = UInt64(1)
        value = UserStruct(
            arc4.String('testName'),
            arc4.UInt64(70),
            arc4.UInt64(2)
        )

        self.box_map_struct[key_0] = value.copy()
        assert self.box_map_struct[key_0].bytes.length == value.bytes.length
        assert self.box_map_struct.length(key_0) == value.bytes.length
        return True
    
    @arc4.abimethod
    def box_map_struct_set(self, key: arc4.UInt64, value: UserStruct) -> bool:
        self.box_map_struct[key]= value.copy()
        assert self.box_map_struct[key] == value
        return True

    @arc4.abimethod
    def box_map_struct_get(self, key: arc4.UInt64) -> UserStruct:
        return self.box_map_struct[key]

    @arc4.abimethod
    def box_map_struct_exists(self, key: arc4.UInt64) -> bool:
        return key in self.box_map_struct
