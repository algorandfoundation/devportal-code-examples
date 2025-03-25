import { arc4, abimethod, Contract, uint64, Uint64, BoxMap } from '@algorandfoundation/algorand-typescript'
import { assert } from '@algorandfoundation/algorand-typescript'

// example: EXAMPLE_STRUCT_IN_BOX
class UserStruct extends arc4.Struct<{
  name: arc4.Str
  id: arc4.UintN64
  asset: arc4.UintN64
}> {}

export default class StructInBoxMap extends Contract {
  public userMap = BoxMap<uint64, UserStruct>({ keyPrefix: 'users' })

  @abimethod()
  public boxMapTest(): boolean {
    const key0 = Uint64(0)
    const value = new UserStruct({
      name: new arc4.Str('testName'),
      id: new arc4.UintN64(70),
      asset: new arc4.UintN64(2),
    })

    this.userMap(key0).value = value.copy()
    assert(this.userMap(key0).length === value.bytes.length, 'Length mismatch')
    assert(this.userMap(key0).length === value.bytes.length, 'Length mismatch')
    return true
  }

  @abimethod()
  public boxMapSet(key: uint64, value: UserStruct): boolean {
    this.userMap(key).value = value.copy()
    assert(this.userMap(key).value === value.copy(), 'Value mismatch')
    return true
  }

  @abimethod()
  public boxMapGet(key: uint64): UserStruct {
    return this.userMap(key).value
  }

  @abimethod()
  public boxMapExists(key: uint64): boolean {
    return this.userMap(key).exists
  }
}
// example: EXAMPLE_STRUCT_IN_BOX
